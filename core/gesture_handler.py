import numpy as np
import time

class GestureHandler:
    def __init__(self):
        self.click_threshold = 8  
        self.click_cooldown = 5  
        self.click_counter = 0
        
        self.middle_finger_click_cooldown = 5
        self.middle_finger_click_counter = 0
        self.middle_finger_click_threshold = 8

        self.double_tap_threshold = 0.6 
        self.last_tap_time = 0
        self.double_tap_cooldown = 0.4

        self.index_hold_threshold = 0.3  
        self.index_hold_start_time = None
        self.index_hold_triggered = False
        self.index_click_detected = False

        self.scroll_threshold = 3  
        self.scroll_counter = 0
        self.scroll_threshold = 4

        self.zoom_threshold = 15
        self.last_distance = None
        self.zoom_cooldown = 5
        self.zoom_counter = 0

        self.swipe_detected = False
        self.swipe_direction = None
        self.swipe_threshold = 15

        self.rotate_threshold = 25
        self.rotate_cooldown = 5
        self.rotate_counter = 0

        self.two_finger_click_threshold = 6
        self.two_finger_click_cooldown = 8
        self.two_finger_click_counter = 0
        self.two_finger_click_window = 2

    def check_index_finger_click(self, y_history, size_history):
        if len(y_history['index']) < 2 or len(size_history) < 2:
            return False

        y_changes = np.diff(y_history['index'])
        max_up = max(y_changes)
        max_down = min(y_changes)
        
        size_changes = np.abs(np.diff(size_history) / np.array(size_history)[:-1])
        size_stable = np.mean(size_changes) <= 0.04
        
        if (size_stable and 
            max_up > self.click_threshold and 
            max_down < -self.click_threshold and 
            self.click_counter == 0):
            
            self.click_counter = self.click_cooldown
            self.index_hold_start_time = time.time()
            self.index_hold_triggered = False
            self.index_click_detected = True
            return True
        return False

    def check_middle_finger_click(self, y_history, size_history):
        if len(y_history['middle']) < 2 or len(size_history) < 2:
            return False

        y_changes = np.diff(y_history['middle'])
        max_up = max(y_changes)
        max_down = min(y_changes)
        
        size_changes = np.abs(np.diff(size_history) / np.array(size_history)[:-1])
        size_stable = np.mean(size_changes) <= 0.04
        
        if (size_stable and 
            max_up > self.middle_finger_click_threshold and 
            max_down < -self.middle_finger_click_threshold and 
            self.middle_finger_click_counter == 0):
            
            self.middle_finger_click_counter = self.middle_finger_click_cooldown
            return True
        return False

    def check_two_finger_click(self, y_history):
        if len(y_history['index']) < self.two_finger_click_window + 1 or len(y_history['middle']) < self.two_finger_click_window + 1:
            return False

        index_y_changes = np.diff(y_history['index'])
        middle_y_changes = np.diff(y_history['middle'])
        
        index_up = max(index_y_changes[-self.two_finger_click_window:])
        index_down = min(index_y_changes[-self.two_finger_click_window:])
        middle_up = max(middle_y_changes[-self.two_finger_click_window:])
        middle_down = min(middle_y_changes[-self.two_finger_click_window:])
        
        if (index_up > self.two_finger_click_threshold and 
            index_down < -self.two_finger_click_threshold and
            middle_up > self.two_finger_click_threshold and 
            middle_down < -self.two_finger_click_threshold and
            self.two_finger_click_counter == 0):
            
            self.two_finger_click_counter = self.two_finger_click_cooldown
            return True
        return False

    def check_double_tap(self, y_history, size_history):
        if len(y_history['index']) < 3 or len(size_history) < 2:
            return False

        current_time = time.time()
        y_changes = np.diff(y_history['index'])
        max_up = max(y_changes)
        max_down = min(y_changes)
        
        size_changes = np.abs(np.diff(size_history) / np.array(size_history)[:-1])
        size_stable = np.mean(size_changes) <= 0.04
        
        if size_stable and max_up > self.click_threshold and max_down < -self.click_threshold:
            if current_time - self.last_tap_time < self.double_tap_threshold:
                if current_time - self.last_tap_time > self.double_tap_cooldown:
                    self.last_tap_time = 0
                    return True
            self.last_tap_time = current_time
        return False

    def check_index_finger_hold(self, hand_movement):
        if self.index_click_detected and self.index_hold_start_time is not None and not self.index_hold_triggered:
            current_time = time.time()
            if (current_time - self.index_hold_start_time >= self.index_hold_threshold and hand_movement < 4):
                self.index_hold_triggered = True
                self.index_click_detected = False
                return True
            elif hand_movement >= 4:
                self.index_hold_start_time = None
                self.index_click_detected = False
        return False

    def check_scroll(self, y_history, index_tip, middle_tip):
        if (self.scroll_counter == 0 and 
            len(y_history['index']) >= 2 and 
            len(y_history['middle']) >= 2):
            
            index_y_change = y_history['index'][0] - y_history['index'][-1]
            middle_y_change = y_history['middle'][0] - y_history['middle'][-1]
            fingers_y_difference = abs(index_tip[1] - middle_tip[1])

            if (abs(index_tip[0] - middle_tip[0]) < 40 and  
                fingers_y_difference < 12 and 
                abs(index_y_change) > self.scroll_threshold and
                abs(middle_y_change) > self.scroll_threshold and
                abs(index_y_change - middle_y_change) < 15):
                
                self.scroll_counter = self.scroll_cooldown
                return 'down' if index_y_change > 0 and middle_y_change > 0 else 'up'
        return None

    def check_zoom(self, index_tip, middle_tip):
        if self.zoom_counter == 0:
            distance_between_fingers = np.linalg.norm(np.array(index_tip) - np.array(middle_tip))
            
            if self.last_distance is not None:
                distance_change = distance_between_fingers - self.last_distance
                if abs(distance_change) > self.zoom_threshold:
                    self.zoom_counter = self.zoom_cooldown
                    self.last_distance = distance_between_fingers
                    return 'out' if distance_change > 0 else 'in'
                    
            self.last_distance = distance_between_fingers
        return None

    def check_rotate(self, x_history, y_history):
        if (self.rotate_counter == 0 and 
            len(x_history['index']) >= 2 and 
            len(x_history['middle']) >= 2):
            
            index_x_changes = np.diff(x_history['index'])
            middle_x_changes = np.diff(x_history['middle'])
            
            fingers_y_difference = abs(y_history['index'][-1] - y_history['middle'][-1])

            if fingers_y_difference < 12:
                index_x_total_change = np.sum(index_x_changes)
                middle_x_total_change = np.sum(middle_x_changes)
                
                if (abs(index_x_total_change) > self.rotate_threshold and
                    abs(middle_x_total_change) > self.rotate_threshold):
                    
                    if index_x_total_change > 0 and middle_x_total_change > 0:
                        self.rotate_counter = self.rotate_cooldown
                        return 'right'
                    elif index_x_total_change < 0 and middle_x_total_change < 0:
                        self.rotate_counter = self.rotate_cooldown
                        return 'left'
        return None

    def check_swipe(self, index_tip, middle_tip, ring_tip, pinky_tip, last_position, is_moving_slowly):
        if last_position is None:
            return None

        horizontal_movement = all(
            abs(tip[0] - last_position[0]) > self.swipe_threshold
            for tip in [index_tip, middle_tip, ring_tip]
        )

        vertical_stability = all(
            abs(tip[1] - last_position[1]) < 15
            for tip in [index_tip, middle_tip, ring_tip]
        )

        if horizontal_movement and vertical_stability and not is_moving_slowly:
            self.swipe_detected = True
            self.swipe_direction = 'right' if index_tip[0] > last_position[0] else 'left'
            return None

        if self.swipe_detected and is_moving_slowly:
            direction = self.swipe_direction
            is_four_finger = abs(pinky_tip[1] - last_position[1]) < 1
            self.swipe_detected = False
            self.swipe_direction = None
            return ('four_finger_' + direction) if is_four_finger else direction

        return None

    def update_cooldowns(self):
        if self.scroll_counter > 0:
            self.scroll_counter -= 1
        if self.click_counter > 0:
            self.click_counter -= 1
        if self.middle_finger_click_counter > 0:
            self.middle_finger_click_counter -= 1
        if self.two_finger_click_counter > 0:
            self.two_finger_click_counter -= 1
        if self.rotate_counter > 0:
            self.rotate_counter -= 1
        if self.zoom_counter > 0:
            self.zoom_counter -= 1

    def reset(self):
        self.click_counter = 0
        self.middle_finger_click_counter = 0
        self.two_finger_click_counter = 0
        self.last_tap_time = 0
        self.index_hold_start_time = None
        self.index_hold_triggered = False
        self.index_click_detected = False
        self.scroll_counter = 0
        self.last_distance = None
        self.swipe_detected = False
        self.swipe_direction = None
        self.rotate_counter = 0
        self.zoom_counter = 0