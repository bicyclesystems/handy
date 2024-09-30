import numpy as np
import pyautogui
from collections import deque

class CursorControl:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.cursor_sensitivity_x = 2.5  # Немного уменьшили чувствительность
        self.cursor_sensitivity_y = 3.0
        self.smoothing_factor = 0.2  # Уменьшили фактор сглаживания для более быстрого отклика
        self.smooth_x, self.smooth_y = pyautogui.position()
        self.cursor_position_history = deque(maxlen=3)  # Уменьшили размер истории
        self.last_finger_position = None
        self.min_speed = 3  # Уменьшили минимальную скорость
        self.max_speed = 80  # Уменьшили максимальную скорость
        self.last_cursor_position = pyautogui.position()
        self.acceleration_factor = 1.5  # Добавили фактор ускорения

    def move_cursor(self, index_finger_tip, surface_center, width, height):
        if self.last_finger_position is None:
            self.last_finger_position = index_finger_tip
            return

        dx = index_finger_tip[0] - self.last_finger_position[0]
        dy = index_finger_tip[1] - self.last_finger_position[1]

        speed = np.sqrt(dx**2 + dy**2)
        speed_factor = min(max((speed - self.min_speed) / (self.max_speed - self.min_speed), 0), 1)
        speed_factor = speed_factor ** self.acceleration_factor  # Применяем нелинейное ускорение

        self.last_finger_position = index_finger_tip

        screen_dx = int(dx * self.cursor_sensitivity_x * (1 + speed_factor))
        screen_dy = int(dy * self.cursor_sensitivity_y * (1 + speed_factor))

        new_x = self.last_cursor_position[0] + screen_dx
        new_y = self.last_cursor_position[1] + screen_dy

        # Применяем ограничение на максимальное перемещение курсора за один кадр
        max_movement = 100  # пикселей
        new_x = max(min(new_x, self.last_cursor_position[0] + max_movement), self.last_cursor_position[0] - max_movement)
        new_y = max(min(new_y, self.last_cursor_position[1] + max_movement), self.last_cursor_position[1] - max_movement)

        self.cursor_position_history.append((new_x, new_y))
        avg_position = np.mean(self.cursor_position_history, axis=0)

        # Применяем экспоненциальное скользящее среднее
        self.smooth_x = int(self.smooth_x * self.smoothing_factor + avg_position[0] * (1 - self.smoothing_factor))
        self.smooth_y = int(self.smooth_y * self.smoothing_factor + avg_position[1] * (1 - self.smoothing_factor))
        
        # Ограничиваем позицию курсора границами экрана
        self.smooth_x = max(0, min(self.smooth_x, self.screen_width))
        self.smooth_y = max(0, min(self.smooth_y, self.screen_height))
        
        # Используем более быстрый метод перемещения курсора
        pyautogui.moveTo(self.smooth_x, self.smooth_y, duration=0, _pause=False)
        self.last_cursor_position = (self.smooth_x, self.smooth_y)

    def reset(self):
        self.cursor_position_history.clear()
        self.last_finger_position = None
        self.last_cursor_position = pyautogui.position()
        self.smooth_x, self.smooth_y = self.last_cursor_position