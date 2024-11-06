import numpy as np
import pyautogui
from collections import deque

class CursorControl:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Уменьшаем базовую чувствительность
        self.cursor_sensitivity_x = 4.5  # было 6
        self.cursor_sensitivity_y = 6  # было 6
        
        # Увеличиваем размер истории для лучшего сглаживания
        self.cursor_position_history = deque(maxlen=6)  # было 4
        self.velocity_history = deque(maxlen=5)  # было 3
        
        self.last_finger_position = None
        # Увеличиваем порог минимальной скорости
        self.min_speed = 2.0  # было 1.2
        self.max_speed = 120
        self.last_cursor_position = pyautogui.position()
        # Уменьшаем фактор ускорения
        self.acceleration_factor = 1.015  # было 1.02
        self.smooth_x, self.smooth_y = pyautogui.position()
        
        # Увеличиваем минимальное сглаживание
        self.min_smoothing = 0.12  # было 0.08
        self.max_smoothing = 0.25  # было 0.15
        
        # Увеличиваем момент инерции
        self.momentum = 0.25  # было 0.15
        self.last_dx = 0
        self.last_dy = 0
        
        # Добавляем порог для игнорирования мелких движений
        self.movement_threshold = 0.8

    def move_cursor(self, index_finger_tip, surface_center, width, height):
        if self.last_finger_position is None:
            self.last_finger_position = index_finger_tip
            return
        
        dx = index_finger_tip[0] - self.last_finger_position[0]
        dy = index_finger_tip[1] - self.last_finger_position[1]
        
        # Игнорируем очень мелкие движения (дрожь)
        if abs(dx) < self.movement_threshold and abs(dy) < self.movement_threshold:
            dx = 0
            dy = 0
        
        # Усиливаем сглаживание для медленных движений
        speed = np.sqrt(dx**2 + dy**2)
        if speed < self.min_speed:
            dx *= 0.5
            dy *= 0.5
        
        dx = dx * (1 - self.momentum) + self.last_dx * self.momentum
        dy = dy * (1 - self.momentum) + self.last_dy * self.momentum
        
        self.last_dx = dx
        self.last_dy = dy
        
        speed = np.sqrt(dx**2 + dy**2)
        speed_factor = np.tanh(speed / (self.max_speed * 0.8))
        speed_factor = speed_factor ** self.acceleration_factor
        
        self.last_finger_position = index_finger_tip
        
        # Уменьшаем boost для медленных движений
        sensitivity_boost = 1.2 if speed > self.max_speed * 0.3 else 1.0
        
        screen_dx = int(dx * self.cursor_sensitivity_x * (0.8 + speed_factor) * sensitivity_boost)
        screen_dy = int(-dy * self.cursor_sensitivity_y * (0.8 + speed_factor) * sensitivity_boost)
        
        new_x = self.last_cursor_position[0] + screen_dx
        new_y = self.last_cursor_position[1] + screen_dy
        
        self.cursor_position_history.append((new_x, new_y))
        
        # Увеличиваем вес последних позиций для более плавного движения
        weights = np.array([1.8 ** i for i in range(len(self.cursor_position_history))])
        weights = weights / np.sum(weights)
        avg_position = np.average(self.cursor_position_history, weights=weights, axis=0)
        
        # Усиливаем сглаживание для медленных движений
        smoothing = self.min_smoothing + (1 - speed_factor) * (self.max_smoothing - self.min_smoothing)
        if speed < self.min_speed:
            smoothing = self.max_smoothing
        elif speed > self.max_speed * 0.3:
            smoothing = self.min_smoothing * 0.7
        
        smoothing_x = smoothing * (0.85 if abs(dx) > abs(dy) else 1.0)
        smoothing_y = smoothing * (0.85 if abs(dy) > abs(dx) else 1.0)
        
        self.smooth_x = int(avg_position[0] * (1 - smoothing_x) + self.smooth_x * smoothing_x)
        self.smooth_y = int(avg_position[1] * (1 - smoothing_y) + self.smooth_y * smoothing_y)
        
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
        self.last_dx = 0
        self.last_dy = 0