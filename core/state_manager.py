from collections import deque
import numpy as np
from additional.utils import (
    calculate_hand_size, smooth_finger_tips, update_state, draw_size_change_graph,
    calculate_hand_center
)

class StateManager:
    def __init__(self):
        self.current_state = "Initializing"
        self.state_transition = {
            "Initializing": 0, "Hand at rest": 0, "Y changing, size stable": 0,
            "Y stable, size changing": 0, "Y changing, size changing": 0
        }
        self.state_transition_threshold = 3
        
        self.y_history = deque(maxlen=10)
        self.size_history = deque(maxlen=10)
        self.threshold_y = 30
        self.threshold_size = 0.025
        
        self.finger_tips_history = [deque(maxlen=2) for _ in range(5)]
        self.size_change_history = deque(maxlen=150)
        
        self.hand_center_history = deque(maxlen=10)
        self.move_threshold = 20

    def process_hand(self, image, hand_landmarks, video_processor, cursor_control, click_handler):
        hand_info = video_processor.hand_api.get_hand_info(image, hand_landmarks)
        
        smoothed_finger_tips = smooth_finger_tips(hand_info['finger_tips'], self.finger_tips_history)
        hand_info['finger_tips'] = smoothed_finger_tips
        
        index_finger_tip = hand_info['finger_tips'][1]
        
        hand_on_surface = video_processor.surface_api.is_point_inside_contour(index_finger_tip)
        hand_status = "On surface" if hand_on_surface else "Off surface"
        
        video_processor.draw_hand_status(image, hand_status)
        
        if hand_on_surface and video_processor.surface_api.is_surface_locked:
            self._process_hand_on_surface(index_finger_tip, hand_landmarks, video_processor, cursor_control, click_handler)
        else:
            self._reset_hand_off_surface()
        
        video_processor.surface_api.update_center(index_finger_tip)
        image = video_processor.hand_api.draw_hand(image, hand_info, hand_landmarks)
        
        return image

    def _process_hand_on_surface(self, index_finger_tip, hand_landmarks, video_processor, cursor_control, click_handler):
        current_y = index_finger_tip[1]
        current_size = calculate_hand_size(hand_landmarks)
        
        self.y_history.append(current_y)
        self.size_history.append(current_size)
        
        hand_center = calculate_hand_center(hand_landmarks, video_processor.width, video_processor.height)
        self.hand_center_history.append(hand_center)
        
        if len(self.y_history) == self.y_history.maxlen and len(self.hand_center_history) == self.hand_center_history.maxlen:
            y_change = max(self.y_history) - min(self.y_history)
            
            size_changes = [abs(self.size_history[i] - self.size_history[i-1]) / self.size_history[i-1] for i in range(1, len(self.size_history))]
            size_changing = any(change > self.threshold_size for change in size_changes)
            
            self.size_change_history.append(size_changes[-1])
            
            hand_movement = np.linalg.norm(self.hand_center_history[-1] - self.hand_center_history[0])
            
            new_state = "Hand at rest"
            if y_change > self.threshold_y and not size_changing:
                new_state = "Y changing, size stable"
                click_handler.handle_click(current_y, self.y_history[0])
            elif hand_movement > self.move_threshold:
                new_state = "Y changing, size changing"
                if video_processor.surface_api.center is not None:
                    cursor_control.move_cursor(index_finger_tip, video_processor.surface_api.center, video_processor.width, video_processor.height)
            elif size_changing:
                new_state = "Y stable, size changing"
            
            self.current_state = update_state(new_state, self.state_transition, self.state_transition_threshold) or self.current_state

    def _reset_hand_off_surface(self):
        self.current_state = "Hand off surface"
        self.y_history.clear()
        self.size_history.clear()
        self.hand_center_history.clear()

    def reset(self):
        self.current_state = "Initializing"
        self.y_history.clear()
        self.size_history.clear()
        self.size_change_history.clear()
        for history in self.finger_tips_history:
            history.clear()
        self.hand_center_history.clear()

    def get_size_change_graph(self, image):
        return draw_size_change_graph(image, self.size_change_history)