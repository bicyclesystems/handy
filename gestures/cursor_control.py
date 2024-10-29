import numpy as np
import pyautogui
from collections import deque

class CursorControl:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.cursor_sensitivity_x = 2.5
        self.cursor_sensitivity_y = 3.0
        self.smoothing_factor = 0.15
        self.smooth_x, self.smooth_y = pyautogui.position()
        self.cursor_position_history = deque(maxlen=4)
        self.velocity_history = deque(maxlen=3)
        self.last_finger_position = None
        self.min_speed = 2
        self.max_speed = 80
        self.last_cursor_position = pyautogui.position()
        self.acceleration_factor = 1.3

    def move_cursor(self, index_finger_tip, surface_center, width, height):
        if self.last_finger_position is None:
            self.last_finger_position = index_finger_tip
            return

        dx = index_finger_tip[0] - self.last_finger_position[0]
        dy = index_finger_tip[1] - self.last_finger_position[1]

        current_velocity = np.sqrt(dx**2 + dy**2)
        self.velocity_history.append(current_velocity)
        avg_velocity = np.mean(self.velocity_history)

        speed = np.sqrt(dx**2 + dy**2)
        speed_factor = np.tanh(speed / self.max_speed)
        speed_factor = speed_factor ** self.acceleration_factor

        self.last_finger_position = index_finger_tip

        screen_dx = int(dx * self.cursor_sensitivity_x * (1 + speed_factor))
        screen_dy = int(dy * self.cursor_sensitivity_y * (1 + speed_factor))

        new_x = self.last_cursor_position[0] + screen_dx
        new_y = self.last_cursor_position[1] + screen_dy

        max_movement = 1000
        new_x = max(min(new_x, self.last_cursor_position[0] + max_movement), self.last_cursor_position[0] - max_movement)
        new_y = max(min(new_y, self.last_cursor_position[1] + max_movement), self.last_cursor_position[1] - max_movement)

        self.cursor_position_history.append((new_x, new_y))
        weights = np.array([1, 2, 3, 4][:len(self.cursor_position_history)])
        weights = weights / np.sum(weights)
        avg_position = np.average(self.cursor_position_history, weights=weights, axis=0)

        adaptive_smoothing = max(0.1, min(0.3, 1.0 - speed_factor))
        self.smooth_x = int(self.smooth_x * adaptive_smoothing + avg_position[0] * (1 - adaptive_smoothing))
        self.smooth_y = int(self.smooth_y * adaptive_smoothing + avg_position[1] * (1 - adaptive_smoothing))

        self.smooth_x = max(0, min(self.smooth_x, self.screen_width))
        self.smooth_y = max(0, min(self.smooth_y, self.screen_height))

        pyautogui.moveTo(self.smooth_x, self.smooth_y, duration=0, _pause=False)
        self.last_cursor_position = (self.smooth_x, self.smooth_y)

    def reset(self):
        self.cursor_position_history.clear()
        self.velocity_history.clear()
        self.last_finger_position = None
        self.last_cursor_position = pyautogui.position()
        self.smooth_x, self.smooth_y = self.last_cursor_position