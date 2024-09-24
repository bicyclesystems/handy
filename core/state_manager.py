from collections import deque
import numpy as np
import time
from additional.utils import (
    calculate_hand_size, smooth_finger_tips, update_state, draw_size_change_graph,
    calculate_hand_center
)

class StateManager:
    def __init__(self):
        self.current_state = "Initializing"
        self.state_transition = {
            "Initializing": 0, "Hand at rest": 0, "Y changing, size stable": 0,
            "Y stable, size changing": 0, "Y changing, size changing": 0,
            "Hand off surface": 0
        }
        self.state_transition_threshold = 3
        
        self.y_history = {
            'index': deque(maxlen=5),
            'middle': deque(maxlen=5),
            'ring': deque(maxlen=5), 
            'pinky': deque(maxlen=5)   
        }
        self.size_history = deque(maxlen=10)
        self.threshold_y = 15
        self.threshold_size = 0.05
        self.threshold_size_change = 0.01 
        
        self.finger_tips_history = [deque(maxlen=2) for _ in range(5)]
        self.size_change_history = deque(maxlen=150)
        
        self.hand_center_history = deque(maxlen=10)
        self.move_threshold = 20

        self.click_threshold = 10 
        self.click_cooldown = 10 
        self.click_counter = 0

        self.last_on_surface_position = None
        self.middle_finger_click_cooldown = 10  
        self.middle_finger_click_counter = 0
        self.middle_finger_click_threshold = 10  

        self.cursor_stability_threshold = 5  
        self.cursor_movement_enabled = True 

        self.two_finger_click_threshold = 8
        self.two_finger_click_cooldown = 15
        self.two_finger_click_counter = 0
        self.two_finger_click_window = 3

        self.double_tap_threshold = 1 
        self.last_tap_time = 0
        self.double_tap_cooldown = 0.5  

        self.index_hold_threshold = 0.5 
        self.index_hold_start_time = None
        self.index_hold_triggered = False
        self.index_click_detected = False

        self.scroll_cooldown = 5
        self.scroll_counter = 0

        self.zoom_threshold = 200  
        self.last_distance = None  
        self.ring_finger_history = deque(maxlen=5)  
        self.swipe_detected = False
        self.swipe_direction = None

    def process_hand(self, image, hand_landmarks, video_processor, cursor_control, click_handler):
        hand_info = video_processor.hand_api.get_hand_info(image, hand_landmarks)
        
        smoothed_finger_tips = smooth_finger_tips(hand_info['finger_tips'], self.finger_tips_history)
        hand_info['finger_tips'] = smoothed_finger_tips
        
        index_finger_tip = hand_info['finger_tips'][1]
        middle_finger_tip = hand_info['finger_tips'][2]
        ring_finger_tip = hand_info['finger_tips'][3]
        pinky_finger_tip = hand_info['finger_tips'][4]  
        
        hand_on_surface = video_processor.surface_api.is_point_inside_contour(index_finger_tip)
        hand_status = "On surface" if hand_on_surface else "Off surface"
        
        video_processor.draw_hand_status(image, hand_status)
        
        if hand_on_surface and video_processor.surface_api.is_surface_locked:
            self._process_hand_on_surface(index_finger_tip, middle_finger_tip, ring_finger_tip, pinky_finger_tip, hand_info, hand_landmarks, video_processor, cursor_control, click_handler)
            self.last_on_surface_position = index_finger_tip
        else:
            self._process_hand_off_surface(cursor_control)
        
        video_processor.surface_api.update_center(index_finger_tip)
        image = video_processor.hand_api.draw_hand(image, hand_info, hand_landmarks)
        
        return image

    def _process_hand_on_surface(self, index_finger_tip, middle_finger_tip, ring_finger_tip, pinky_finger_tip, hand_info, hand_landmarks, video_processor, cursor_control, click_handler):
        current_size = calculate_hand_size(hand_landmarks)
        
        self.y_history['index'].append(index_finger_tip[1])
        self.y_history['middle'].append(middle_finger_tip[1])
        self.y_history['ring'].append(ring_finger_tip[1])  
        self.y_history['pinky'].append(pinky_finger_tip[1]) 
        self.size_history.append(current_size)

        hand_center = calculate_hand_center(hand_landmarks, video_processor.width, video_processor.height)
        self.hand_center_history.append(hand_center)

        if len(self.y_history['index']) == self.y_history['index'].maxlen and len(self.size_history) == self.size_history.maxlen:
            size_changes = np.diff(self.size_history) / np.array(self.size_history)[:-1]
            size_stable = np.mean(np.abs(size_changes)) <= self.threshold_size
            
            index_y_change = self.y_history['index'][0] - self.y_history['index'][-1]
            middle_y_change = self.y_history['middle'][0] - self.y_history['middle'][-1]
            ring_y_change = self.y_history['ring'][0] - self.y_history['ring'][-1]
            pinky_y_change = self.y_history['pinky'][0] - self.y_history['pinky'][-1]
            size_change = (self.size_history[-1] - self.size_history[0]) / self.size_history[0]

            hand_movement = np.linalg.norm(self.hand_center_history[-1] - self.hand_center_history[0])
            is_moving_slowly = hand_movement < self.cursor_stability_threshold * 0.5

            is_swiping = (abs(index_y_change) < 20 and abs(middle_y_change) < 20 and abs(ring_y_change) < 20 and
                          abs(index_finger_tip[0] - self.last_on_surface_position[0]) > 20 and
                          abs(middle_finger_tip[0] - self.last_on_surface_position[0]) > 20 and
                          abs(ring_finger_tip[0] - self.last_on_surface_position[0]) > 20)

            if is_swiping and not is_moving_slowly:
                self.swipe_detected = True 
                self.swipe_direction = 'right' if index_finger_tip[0] > self.last_on_surface_position[0] else 'left'

            if self.swipe_detected and is_moving_slowly:
                if abs(pinky_y_change) < 1:
                    print(f"{self.swipe_direction.capitalize()} Four-Finger Swipe")
                else:
                    print(f"Swipe {self.swipe_direction.capitalize()}")
                self.swipe_detected = False
                self.swipe_direction = None

            if self.scroll_counter == 0:
                if index_y_change > self.threshold_y * 1.5 and middle_y_change > self.threshold_y * 1.5 and size_change > self.threshold_size_change:
                    print("Down Scroll")
                    self.scroll_counter = self.scroll_cooldown
                elif index_y_change < -self.threshold_y * 1.5 and middle_y_change < -self.threshold_y * 1.5 and size_change < -self.threshold_size_change:
                    print("Up Scroll")
                    self.scroll_counter = self.scroll_cooldown

            distance_between_fingers = np.linalg.norm(np.array(index_finger_tip) - np.array(middle_finger_tip))
            if self.last_distance is not None:
                hand_movement = np.linalg.norm(self.hand_center_history[-1] - self.hand_center_history[0])
                if hand_movement < self.cursor_stability_threshold: 
                    if distance_between_fingers < self.last_distance - 50: 
                        print("Zoom In")
                    elif distance_between_fingers > self.last_distance + 50: 
                        print("Zoom Out")
            self.last_distance = distance_between_fingers  
            
            hand_movement = np.linalg.norm(self.hand_center_history[-1] - self.hand_center_history[0])
            
            if hand_movement < self.cursor_stability_threshold:
                if size_stable:
                    if self._check_two_finger_click():
                        self._perform_click("Two Fingers")
                    elif self.two_finger_click_counter == 0:
                        if self._check_double_tap():
                            self._perform_double_tap()
                        elif self._check_index_finger_click(index_finger_tip, click_handler):
                            self._perform_click("Index Finger")
                        elif self._check_middle_finger_click(middle_finger_tip):
                            self._perform_click("Middle Finger")
                    
                    self._check_index_finger_hold(hand_movement)
            else:
                self.index_hold_start_time = None
                self.index_hold_triggered = False
                self.index_click_detected = False
                
                if video_processor.surface_api.center is not None and self.cursor_movement_enabled:
                    cursor_control.move_cursor(index_finger_tip, video_processor.surface_api.center, video_processor.width, video_processor.height)
            
            self.size_change_history.append(np.mean(size_changes))
            
            new_state = "Hand at rest"
            if abs(self.y_history['index'][0] - self.y_history['index'][-1]) > self.threshold_y and not size_stable:
                new_state = "Y changing, size stable"
            elif hand_movement > self.move_threshold * 0.5:
                new_state = "Y changing, size changing"
            elif size_stable:
                new_state = "Y stable, size changing"
            
            self.current_state = update_state(new_state, self.state_transition, self.state_transition_threshold) or self.current_state
            
            if self.scroll_counter > 0:
                self.scroll_counter -= 1
            if self.click_counter > 0:
                self.click_counter -= 1
            if self.middle_finger_click_counter > 0:
                self.middle_finger_click_counter -= 1
            if self.two_finger_click_counter > 0:
                self.two_finger_click_counter -= 1
                
    def _check_index_finger_click(self, index_finger_tip, click_handler):
        y_change = self.y_history['index'][0] - self.y_history['index'][-1]
        y_change_back = self.y_history['index'][-1] - self.y_history['index'][-2]
        
        size_changes = np.abs(np.diff(self.size_history) / np.array(self.size_history)[:-1])
        size_stable = np.mean(size_changes) <= self.threshold_size
        
        if size_stable and y_change > self.click_threshold and y_change_back < -self.click_threshold and self.click_counter == 0:
            self.cursor_movement_enabled = False  
            self.click_counter = self.click_cooldown
            self.cursor_movement_enabled = True 
            self.index_hold_start_time = time.time()
            self.index_hold_triggered = False
            self.index_click_detected = True
            return True
        return False

    def _check_middle_finger_click(self, middle_finger_tip):
        y_changes = np.diff(self.y_history['middle'])
        max_up = max(y_changes)
        max_down = min(y_changes)
        
        size_changes = np.abs(np.diff(self.size_history) / np.array(self.size_history)[:-1])
        size_stable = np.mean(size_changes) <= self.threshold_size
        
        if size_stable and max_up > self.middle_finger_click_threshold and max_down < -self.middle_finger_click_threshold and self.middle_finger_click_counter == 0:
            self.cursor_movement_enabled = False 
            self.middle_finger_click_counter = self.middle_finger_click_cooldown
            self.cursor_movement_enabled = True 
            return True
        return False

    def _check_two_finger_click(self):
        index_y_changes = np.diff(self.y_history['index'])
        middle_y_changes = np.diff(self.y_history['middle'])
        
        index_up = max(index_y_changes[-self.two_finger_click_window:])
        index_down = min(index_y_changes[-self.two_finger_click_window:])
        middle_up = max(middle_y_changes[-self.two_finger_click_window:])
        middle_down = min(middle_y_changes[-self.two_finger_click_window:])
        
        size_changes = np.abs(np.diff(self.size_history) / np.array(self.size_history)[:-1])
        size_stable = np.mean(size_changes) <= self.threshold_size
        
        if (size_stable and
            index_up > self.two_finger_click_threshold and index_down < -self.two_finger_click_threshold and
            middle_up > self.two_finger_click_threshold and middle_down < -self.two_finger_click_threshold and
            self.two_finger_click_counter == 0):
            self.cursor_movement_enabled = False
            self.two_finger_click_counter = self.two_finger_click_cooldown
            self.cursor_movement_enabled = True
            return True
        return False

    def _check_double_tap(self):
        current_time = time.time()
        y_change = self.y_history['index'][0] - self.y_history['index'][-1]
        y_change_back = self.y_history['index'][-1] - self.y_history['index'][-2]
        
        size_changes = np.abs(np.diff(self.size_history) / np.array(self.size_history)[:-1])
        size_stable = np.mean(size_changes) <= self.threshold_size
        
        if size_stable and y_change > self.click_threshold and y_change_back < -self.click_threshold:
            if current_time - self.last_tap_time < self.double_tap_threshold:
                if current_time - self.last_tap_time > self.double_tap_cooldown:
                    self.last_tap_time = 0
                    return True
            self.last_tap_time = current_time
        return False

    def _check_index_finger_hold(self, hand_movement):
        if self.index_click_detected and self.index_hold_start_time is not None and not self.index_hold_triggered:
            current_time = time.time()
            if current_time - self.index_hold_start_time >= self.index_hold_threshold and hand_movement < self.cursor_stability_threshold:
                print("Index Hold")
                self.index_hold_triggered = True
                self.index_click_detected = False
            elif hand_movement >= self.cursor_stability_threshold:
                self.index_hold_start_time = None
                self.index_click_detected = False

    def _perform_click(self, finger_name):
        print(f"Click with {finger_name}")

    def _perform_double_tap(self):
        print("Double Tap")

    def _process_hand_off_surface(self, cursor_control):
        new_state = "Hand off surface"
        self.current_state = update_state(new_state, self.state_transition, self.state_transition_threshold) or self.current_state
        cursor_control.reset()

    def reset(self):
        self.current_state = "Initializing"
        self.y_history['index'].clear()
        self.y_history['middle'].clear()
        self.y_history['ring'].clear()
        self.y_history['pinky'].clear()
        self.size_history.clear()
        self.size_change_history.clear()
        for history in self.finger_tips_history:
            history.clear()
        self.hand_center_history.clear()
        self.click_counter = 0
        self.middle_finger_click_counter = 0
        self.two_finger_click_counter = 0
        self.last_on_surface_position = None
        self.last_tap_time = 0
        self.index_hold_start_time = None
        self.index_hold_triggered = False
        self.index_click_detected = False
        self.scroll_counter = 0
        self.last_distance = None
        self.swipe_detected = False
        self.swipe_direction = None

    def get_size_change_graph(self, image):
        return draw_size_change_graph(image, self.size_change_history)