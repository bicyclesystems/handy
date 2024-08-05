import numpy as np
import pyautogui
from collections import deque

class CursorControl:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.cursor_sensitivity_x = 2.0
        self.cursor_sensitivity_y = 2.5
        self.smoothing_factor = 0.3
        self.smooth_x, self.smooth_y = 0, 0
        self.cursor_position_history = deque(maxlen=5)
        self.previous_finger_position = None
        self.min_speed = 5
        self.max_speed = 100

    def move_cursor(self, index_finger_tip, surface_center, width, height):
        cX, cY = surface_center
        norm_x = (index_finger_tip[0] - cX) / (width / 2)
        norm_y = (index_finger_tip[1] - cY) / (height / 2)
        
        if self.previous_finger_position:
            dx = index_finger_tip[0] - self.previous_finger_position[0]
            dy = index_finger_tip[1] - self.previous_finger_position[1]
            speed = np.sqrt(dx**2 + dy**2)
            
            speed_factor = min(max((speed - self.min_speed) / (self.max_speed - self.min_speed), 0), 1)
            speed_factor = speed_factor ** 2
        else:
            speed_factor = 0.5

        self.previous_finger_position = index_finger_tip

        screen_x = int(self.screen_width * (0.5 + norm_x * 0.5 * self.cursor_sensitivity_x * (1 + speed_factor)))
        screen_y = int(self.screen_height * (0.5 + norm_y * 0.5 * self.cursor_sensitivity_y * (1 + speed_factor)))

        self.cursor_position_history.append((screen_x, screen_y))
        avg_position = np.mean(self.cursor_position_history, axis=0)
        self.smooth_x = int(self.smooth_x * self.smoothing_factor + avg_position[0] * (1 - self.smoothing_factor))
        self.smooth_y = int(self.smooth_y * self.smoothing_factor + avg_position[1] * (1 - self.smoothing_factor))
        
        pyautogui.moveTo(self.smooth_x, self.smooth_y, duration=0.01, _pause=False)

    def reset(self):
        self.cursor_position_history.clear()
        self.previous_finger_position = None