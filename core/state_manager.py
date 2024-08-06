# bad index finger clicking

from collections import deque
import numpy as np
import pyautogui
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
            'middle': deque(maxlen=5)
        }
        self.size_history = deque(maxlen=10)
        self.threshold_y = 15
        self.threshold_size = 0.05
        
        self.finger_tips_history = [deque(maxlen=2) for _ in range(5)]
        self.size_change_history = deque(maxlen=150)
        
        self.hand_center_history = deque(maxlen=10)
        self.move_threshold = 20

        self.click_threshold = 20  
        self.click_cooldown = 10 
        self.click_counter = 0

        self.last_on_surface_position = None
        self.middle_finger_click_cooldown = 20  
        self.middle_finger_click_counter = 0
        self.middle_finger_click_threshold = 15  

        self.cursor_stability_threshold = 5  

    def process_hand(self, image, hand_landmarks, video_processor, cursor_control, click_handler):
        hand_info = video_processor.hand_api.get_hand_info(image, hand_landmarks)
        
        smoothed_finger_tips = smooth_finger_tips(hand_info['finger_tips'], self.finger_tips_history)
        hand_info['finger_tips'] = smoothed_finger_tips
        
        index_finger_tip = hand_info['finger_tips'][1]
        middle_finger_tip = hand_info['finger_tips'][2]
        
        hand_on_surface = video_processor.surface_api.is_point_inside_contour(index_finger_tip)
        hand_status = "On surface" if hand_on_surface else "Off surface"
        
        video_processor.draw_hand_status(image, hand_status)
        
        if hand_on_surface and video_processor.surface_api.is_surface_locked:
            self._process_hand_on_surface(index_finger_tip, middle_finger_tip, hand_landmarks, video_processor, cursor_control, click_handler)
            self.last_on_surface_position = index_finger_tip
        else:
            self._process_hand_off_surface(cursor_control)
        
        video_processor.surface_api.update_center(index_finger_tip)
        image = video_processor.hand_api.draw_hand(image, hand_info, hand_landmarks)
        
        return image

    def _process_hand_on_surface(self, index_finger_tip, middle_finger_tip, hand_landmarks, video_processor, cursor_control, click_handler):
        current_size = calculate_hand_size(hand_landmarks)
        
        self.y_history['index'].append(index_finger_tip[1])
        self.y_history['middle'].append(middle_finger_tip[1])
        self.size_history.append(current_size)
        
        hand_center = calculate_hand_center(hand_landmarks, video_processor.width, video_processor.height)
        self.hand_center_history.append(hand_center)
        
        if len(self.y_history['index']) == self.y_history['index'].maxlen and len(self.size_history) == self.size_history.maxlen:
            size_changes = np.abs(np.diff(self.size_history) / np.array(self.size_history)[:-1])
            size_changing = np.mean(size_changes) > self.threshold_size
            
            hand_movement = np.linalg.norm(self.hand_center_history[-1] - self.hand_center_history[0])
            
            if hand_movement < self.cursor_stability_threshold:
                self._check_index_finger_click(index_finger_tip, click_handler)
                self._check_middle_finger_click(middle_finger_tip)
            else:
                if video_processor.surface_api.center is not None:
                    cursor_control.move_cursor(index_finger_tip, video_processor.surface_api.center, video_processor.width, video_processor.height)
            
            self.size_change_history.append(np.mean(size_changes))
            
            new_state = "Hand at rest"
            if abs(self.y_history['index'][0] - self.y_history['index'][-1]) > self.threshold_y and not size_changing:
                new_state = "Y changing, size stable"
            elif hand_movement > self.move_threshold * 0.5:
                new_state = "Y changing, size changing"
            elif size_changing:
                new_state = "Y stable, size changing"
            
            self.current_state = update_state(new_state, self.state_transition, self.state_transition_threshold) or self.current_state
            
            if self.click_counter > 0:
                self.click_counter -= 1
            if self.middle_finger_click_counter > 0:
                self.middle_finger_click_counter -= 1

    def _check_index_finger_click(self, index_finger_tip, click_handler):
        y_change = self.y_history['index'][0] - self.y_history['index'][-1]
        y_change_back = self.y_history['index'][-1] - self.y_history['index'][-2]
        
        if y_change > self.click_threshold and y_change_back < -self.click_threshold and self.click_counter == 0:
            self._perform_click()
            self.click_counter = self.click_cooldown
            print(f"Click performed! Y-change up: {y_change}, Y-change down: {y_change_back}")

    def _check_middle_finger_click(self, middle_finger_tip):
        y_changes = np.diff(self.y_history['middle'])
        max_up = max(y_changes)
        max_down = min(y_changes)
        
        if max_up > self.middle_finger_click_threshold and max_down < -self.middle_finger_click_threshold and self.middle_finger_click_counter == 0:
            self.middle_finger_click_counter = self.middle_finger_click_cooldown
            print(f"Middle Finger Click! Y-change up: {max_up}, Y-change down: {max_down}")

    def _perform_click(self):
        pyautogui.click()

    def _process_hand_off_surface(self, cursor_control):
        new_state = "Hand off surface"
        self.current_state = update_state(new_state, self.state_transition, self.state_transition_threshold) or self.current_state
        cursor_control.reset()

    def reset(self):
        self.current_state = "Initializing"
        self.y_history['index'].clear()
        self.y_history['middle'].clear()
        self.size_history.clear()
        self.size_change_history.clear()
        for history in self.finger_tips_history:
            history.clear()
        self.hand_center_history.clear()
        self.click_counter = 0
        self.middle_finger_click_counter = 0
        self.last_on_surface_position = None

    def get_size_change_graph(self, image):
        return draw_size_change_graph(image, self.size_change_history)


# bad cursor moving



# from collections import deque
# import numpy as np
# import pyautogui
# from additional.utils import (
#     calculate_hand_size, smooth_finger_tips, update_state, draw_size_change_graph,
#     calculate_hand_center
# )

# class StateManager:
#     def __init__(self):
#         self.current_state = "Initializing"
#         self.state_transition = {
#             "Initializing": 0, "Hand at rest": 0, "Y changing, size stable": 0,
#             "Y stable, size changing": 0, "Y changing, size changing": 0,
#             "Hand off surface": 0
#         }
#         self.state_transition_threshold = 3
        
#         self.y_history = {
#             'index': deque(maxlen=5),
#             'middle': deque(maxlen=5)
#         }
#         self.size_history = deque(maxlen=10) 
#         self.threshold_y = 15
#         self.threshold_size = 0.05 
        
#         self.finger_tips_history = [deque(maxlen=2) for _ in range(5)]
#         self.size_change_history = deque(maxlen=150)
        
#         self.hand_center_history = deque(maxlen=10)
#         self.move_threshold = 20

#         self.click_threshold = 15
#         self.click_cooldown = 5
#         self.click_counter = 0

#         self.last_on_surface_position = None
#         self.middle_finger_click_cooldown = 15
#         self.middle_finger_click_counter = 0
#         self.middle_finger_click_threshold = 10

#     def process_hand(self, image, hand_landmarks, video_processor, cursor_control, click_handler):
#         hand_info = video_processor.hand_api.get_hand_info(image, hand_landmarks)
        
#         smoothed_finger_tips = smooth_finger_tips(hand_info['finger_tips'], self.finger_tips_history)
#         hand_info['finger_tips'] = smoothed_finger_tips
        
#         index_finger_tip = hand_info['finger_tips'][1]
#         middle_finger_tip = hand_info['finger_tips'][2]
        
#         hand_on_surface = video_processor.surface_api.is_point_inside_contour(index_finger_tip)
#         hand_status = "On surface" if hand_on_surface else "Off surface"
        
#         video_processor.draw_hand_status(image, hand_status)
        
#         if hand_on_surface and video_processor.surface_api.is_surface_locked:
#             self._process_hand_on_surface(index_finger_tip, middle_finger_tip, hand_landmarks, video_processor, cursor_control, click_handler)
#             self.last_on_surface_position = index_finger_tip
#         else:
#             self._process_hand_off_surface(cursor_control)
        
#         video_processor.surface_api.update_center(index_finger_tip)
#         image = video_processor.hand_api.draw_hand(image, hand_info, hand_landmarks)
        
#         return image

#     def _process_hand_on_surface(self, index_finger_tip, middle_finger_tip, hand_landmarks, video_processor, cursor_control, click_handler):
#         current_size = calculate_hand_size(hand_landmarks)
        
#         self.y_history['index'].append(index_finger_tip[1])
#         self.y_history['middle'].append(middle_finger_tip[1])
#         self.size_history.append(current_size)
        
#         hand_center = calculate_hand_center(hand_landmarks, video_processor.width, video_processor.height)
#         self.hand_center_history.append(hand_center)
        
#         if len(self.y_history['index']) == self.y_history['index'].maxlen and len(self.size_history) == self.size_history.maxlen:
#             size_changes = np.abs(np.diff(self.size_history) / np.array(self.size_history)[:-1])
#             size_changing = np.mean(size_changes) > self.threshold_size  # Изменено на среднее значение изменений
            
#             self._check_index_finger_click(index_finger_tip, click_handler)
#             self._check_middle_finger_click(middle_finger_tip)
            
#             self.size_change_history.append(np.mean(size_changes))
            
#             hand_movement = np.linalg.norm(self.hand_center_history[-1] - self.hand_center_history[0])
            
#             new_state = "Hand at rest"
#             if abs(self.y_history['index'][0] - self.y_history['index'][-1]) > self.threshold_y and not size_changing:
#                 new_state = "Y changing, size stable"
#             elif hand_movement > self.move_threshold * 0.5:
#                 new_state = "Y changing, size changing"
#                 if video_processor.surface_api.center is not None:
#                     cursor_control.move_cursor(index_finger_tip, video_processor.surface_api.center, video_processor.width, video_processor.height)
#             elif size_changing:
#                 new_state = "Y stable, size changing"
            
#             self.current_state = update_state(new_state, self.state_transition, self.state_transition_threshold) or self.current_state
            
#             if self.click_counter > 0:
#                 self.click_counter -= 1
#             if self.middle_finger_click_counter > 0:
#                 self.middle_finger_click_counter -= 1

#     def _check_index_finger_click(self, index_finger_tip, click_handler):
#         y_change = self.y_history['index'][0] - self.y_history['index'][-1]
#         y_change_back = self.y_history['index'][-1] - self.y_history['index'][-2]
        
#         if y_change > self.click_threshold and y_change_back < -self.click_threshold and self.click_counter == 0:
#             self._perform_click()
#             self.click_counter = self.click_cooldown
#             print(f"Click performed! Y-change up: {y_change}, Y-change down: {y_change_back}")

#     def _check_middle_finger_click(self, middle_finger_tip):
#         y_changes = np.diff(self.y_history['middle'])
#         max_up = max(y_changes)
#         max_down = min(y_changes)
        
#         if max_up > self.middle_finger_click_threshold and max_down < -self.middle_finger_click_threshold and self.middle_finger_click_counter == 0:
#             self.middle_finger_click_counter = self.middle_finger_click_cooldown
#             print(f"Middle Finger Click! Y-change up: {max_up}, Y-change down: {max_down}")

#     def _perform_click(self):
#         pyautogui.click()

#     def _process_hand_off_surface(self, cursor_control):
#         new_state = "Hand off surface"
#         self.current_state = update_state(new_state, self.state_transition, self.state_transition_threshold) or self.current_state
#         cursor_control.reset()

#     def reset(self):
#         self.current_state = "Initializing"
#         self.y_history['index'].clear()
#         self.y_history['middle'].clear()
#         self.size_history.clear()
#         self.size_change_history.clear()
#         for history in self.finger_tips_history:
#             history.clear()
#         self.hand_center_history.clear()
#         self.click_counter = 0
#         self.middle_finger_click_counter = 0
#         self.last_on_surface_position = None

#     def get_size_change_graph(self, image):
#         return draw_size_change_graph(image, self.size_change_history)