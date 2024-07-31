import numpy as np
import pyautogui
from collections import deque

class CursorControl:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.cursor_sensitivity = 2.0
        self.smoothing_factor = 0.9
        self.smooth_x, self.smooth_y = 0, 0
        self.cursor_position_history = deque(maxlen=5)

    def move_cursor(self, index_finger_tip, surface_center, width, height):
        cX, cY = surface_center
        norm_x = (index_finger_tip[0] - cX) / (width / 2)
        norm_y = (index_finger_tip[1] - cY) / (height / 2)
        
        screen_x = int(self.screen_width * (0.5 + norm_x * 0.5 * self.cursor_sensitivity))
        screen_y = int(self.screen_height * (0.5 + norm_y * 0.5 * self.cursor_sensitivity))

        self.cursor_position_history.append((screen_x, screen_y))
        avg_position = np.mean(self.cursor_position_history, axis=0)
        self.smooth_x = int(avg_position[0])
        self.smooth_y = int(avg_position[1])
        
        pyautogui.moveTo(self.smooth_x, self.smooth_y, duration=0.01, _pause=False)

    def reset(self):
        self.cursor_position_history.clear()