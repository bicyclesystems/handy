import numpy as np
import pyautogui
from collections import deque

class CursorControl:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.cursor_sensitivity_x = 3.0  
        self.cursor_sensitivity_y = 3.5 
        self.smoothing_factor = 0.3
        self.smooth_x, self.smooth_y = 0, 0
        self.cursor_position_history = deque(maxlen=5)
        self.previous_finger_position = None
        self.min_speed = 5
        self.max_speed = 100
        self.last_cursor_position = pyautogui.position()
        self.last_finger_position = None

    def move_cursor(self, index_finger_tip, surface_center, width, height):
        cX, cY = surface_center
        norm_x = (index_finger_tip[0] - cX) / (width / 2)
        norm_y = (index_finger_tip[1] - cY) / (height / 2)
        
        if self.last_finger_position is not None:
            dx = index_finger_tip[0] - self.last_finger_position[0]
            dy = index_finger_tip[1] - self.last_finger_position[1]
        else:
            dx, dy = 0, 0

        speed = np.sqrt(dx**2 + dy**2)
        speed_factor = min(max((speed - self.min_speed) / (self.max_speed - self.min_speed), 0), 1)
        speed_factor = speed_factor ** 2

        self.last_finger_position = index_finger_tip

        screen_dx = int(dx * self.cursor_sensitivity_x * (1 + speed_factor))
        screen_dy = int(dy * self.cursor_sensitivity_y * (1 + speed_factor))

        screen_x = self.last_cursor_position[0] + screen_dx
        screen_y = self.last_cursor_position[1] + screen_dy

        self.cursor_position_history.append((screen_x, screen_y))
        avg_position = np.mean(self.cursor_position_history, axis=0)
        self.smooth_x = int(self.smooth_x * self.smoothing_factor + avg_position[0] * (1 - self.smoothing_factor))
        self.smooth_y = int(self.smooth_y * self.smoothing_factor + avg_position[1] * (1 - self.smoothing_factor))
        
        self.smooth_x = max(0, min(self.smooth_x, self.screen_width))
        self.smooth_y = max(0, min(self.smooth_y, self.screen_height))
        
        pyautogui.moveTo(self.smooth_x, self.smooth_y, duration=0.01, _pause=False)
        self.last_cursor_position = (self.smooth_x, self.smooth_y)

    def reset(self):
        self.cursor_position_history.clear()
        self.last_finger_position = None
        self.last_cursor_position = pyautogui.position()