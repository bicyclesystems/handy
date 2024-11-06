from .gesture_handler import GestureHandler
from .history_manager import HistoryManager
import pyautogui
from additional.utils import (
    calculate_hand_size, smooth_finger_tips, update_state,
    calculate_hand_center, draw_size_change_graph
)

class StateManager:
    def __init__(self):
        self.current_state = "Initializing"
        self.state_transition = {
            "Initializing": 0, "Hand at rest": 0, "Y changing, size stable": 0,
            "Y stable, size changing": 0, "Y changing, size changing": 0,
            "Hand off surface": 0
        }
        self.state_transition_threshold = 2
        
        self.history = HistoryManager()
        self.gesture = GestureHandler()
        
        self.last_on_surface_position = None
        self.cursor_stability_threshold = 2.0  
        self.cursor_movement_enabled = True
        self.move_threshold = 12
        
        pyautogui.FAILSAFE = False

    def process_hand(self, image, hand_landmarks, video_processor, cursor_control, click_handler):
        hand_info = video_processor.hand_api.get_hand_info(image, hand_landmarks)
        smoothed_finger_tips = smooth_finger_tips(hand_info['finger_tips'], self.history.finger_tips_history)
        hand_info['finger_tips'] = smoothed_finger_tips
        
        index_finger_tip = hand_info['finger_tips'][1]
        middle_finger_tip = hand_info['finger_tips'][2]
        ring_finger_tip = hand_info['finger_tips'][3]
        pinky_finger_tip = hand_info['finger_tips'][4]
        
        hand_on_surface = video_processor.surface_api.is_point_inside_contour(index_finger_tip)
        hand_status = "On surface" if hand_on_surface else "Off surface"
        video_processor.draw_hand_status(image, hand_status)
        
        if hand_on_surface and video_processor.surface_api.is_surface_locked:
            self._process_hand_on_surface(
                index_finger_tip, middle_finger_tip, ring_finger_tip, pinky_finger_tip,
                hand_info, hand_landmarks, video_processor, cursor_control, click_handler
            )
            self.last_on_surface_position = index_finger_tip
        else:
            self._process_hand_off_surface(cursor_control)
        
        video_processor.surface_api.update_center(index_finger_tip)
        return video_processor.hand_api.draw_hand(image, hand_info, hand_landmarks)

    def _process_hand_on_surface(self, index_tip, middle_tip, ring_tip, pinky_tip, 
                               hand_info, hand_landmarks, video_processor, cursor_control, click_handler):
        current_size = calculate_hand_size(hand_landmarks)
        hand_center = calculate_hand_center(hand_landmarks, video_processor.width, video_processor.height)
        self.history.update_positions(index_tip, middle_tip, ring_tip, pinky_tip, current_size, hand_center)
        
        if not self._process_gestures(index_tip, middle_tip, ring_tip, pinky_tip, 
                                    video_processor, cursor_control, click_handler):
            self._handle_cursor_movement(index_tip, video_processor, cursor_control)
        
        self._update_state()
        self.gesture.update_cooldowns()

    def _process_gestures(self, index_tip, middle_tip, ring_tip, pinky_tip, 
                         video_processor, cursor_control, click_handler):
        hand_movement = self.history.get_movement_amount()
        is_moving_slowly = hand_movement < self.cursor_stability_threshold * 0.5
        
        result = self.gesture.check_rotate(self.history.x_history, self.history.y_history)
        if result:
            print(f"Rotate {result.capitalize()}")
            return True
            
        result = self.gesture.check_swipe(index_tip, middle_tip, ring_tip, pinky_tip,
                                        self.last_on_surface_position, is_moving_slowly)
        if result:
            if 'four_finger' in result:
                print(f"{result.replace('_', ' ').title()} Swipe")
            else:
                print(f"Swipe {result.capitalize()}")
            return True
            
        result = self.gesture.check_scroll(self.history.y_history, index_tip, middle_tip)
        if result:
            print(f"{result.capitalize()} Scroll")
            return True
            
        result = self.gesture.check_zoom(index_tip, middle_tip)
        if result:
            print(f"Zoom {result.capitalize()}")
            return True
            
        if hand_movement < self.cursor_stability_threshold:
            if self.history.is_size_stable():
                return self._handle_clicks(index_tip, middle_tip, click_handler, hand_movement)
        else:
            self._reset_click_state()
            
        return False

    def _handle_clicks(self, index_tip, middle_tip, click_handler, hand_movement):
        if self.gesture.check_two_finger_click(self.history.y_history):
            print("Click with Two Fingers")
            pyautogui.click(button='middle')
            return True
            
        if self.gesture.two_finger_click_counter == 0:
            if self.gesture.check_double_tap(self.history.y_history, self.history.size_history):
                print("Double Tap")
                pyautogui.doubleClick()
                return True
                
            if self.gesture.check_index_finger_click(self.history.y_history, self.history.size_history):
                print("Click with Index Finger")
                pyautogui.click(button='left')
                return True
                
            if self.gesture.check_middle_finger_click(self.history.y_history, self.history.size_history):
                print("Click with Middle Finger")
                pyautogui.click(button='right')
                return True
        
        if self.gesture.check_index_finger_hold(hand_movement):
            print("Index Hold")
            pyautogui.mouseDown()
            return True
            
        return False

    def _handle_cursor_movement(self, index_tip, video_processor, cursor_control):
        if video_processor.surface_api.center is not None:
            cursor_control.move_cursor(
                index_tip,
                video_processor.surface_api.center,
                video_processor.width,
                video_processor.height
            )

    def _update_state(self):
        hand_movement = self.history.get_movement_amount()
        size_stable = self.history.is_size_stable()
        
        new_state = "Hand at rest"
        if abs(self.history.y_history['index'][0] - self.history.y_history['index'][-1]) > self.history.threshold_y:
            if not size_stable:
                new_state = "Y changing, size stable"
        elif hand_movement > self.move_threshold * 0.5:
            new_state = "Y changing, size changing"
        elif size_stable:
            new_state = "Y stable, size changing"
            
        self.current_state = update_state(new_state, self.state_transition, 
                                        self.state_transition_threshold) or self.current_state

    def _process_hand_off_surface(self, cursor_control):
        new_state = "Hand off surface"
        self.current_state = update_state(new_state, self.state_transition, 
                                        self.state_transition_threshold) or self.current_state
        cursor_control.reset()

    def _reset_click_state(self):
        self.gesture.index_hold_start_time = None
        self.gesture.index_hold_triggered = False
        self.gesture.index_click_detected = False

    def reset(self):
        self.current_state = "Initializing"
        self.history.reset()
        self.gesture.reset()
        self.last_on_surface_position = None
        self.cursor_movement_enabled = True

    def get_size_change_graph(self, image):
        return draw_size_change_graph(image, self.history.size_change_history)