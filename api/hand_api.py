# import cv2
# import mediapipe as mp
# import numpy as np

# class HandAPI:
#     def __init__(self, surface_api):
#         self.mp_hands = mp.solutions.hands
#         self.hands = self.mp_hands.Hands(
#             static_image_mode=False, 
#             max_num_hands=1,
#             min_detection_confidence=0.5,
#             min_tracking_confidence=0.5
#         )
#         self.surface_api = surface_api
#         self.finger_axis_length = 50  
#         self.image_width = 0
#         self.image_height = 0
#         self.finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
#         self.show_axes = {name: True for name in self.finger_names}
#         self.button_size = (100, 30)
#         self.button_margin = 10
        
#         self.prev_landmarks = None
#         self.smooth_factor = 0.5  # Уменьшили фактор сглаживания
#         self.velocity_filter = 0.7  # Добавили фильтр скорости
#         self.prev_velocity = None
        
#         self.clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
#         self.contrast_alpha = 1.2
#         self.contrast_beta = 10

#         self.landmark_colors = [
#             (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255),
#             (0, 255, 255), (128, 0, 0), (0, 128, 0), (0, 0, 128), (128, 128, 0),
#             (128, 0, 128), (0, 128, 128), (255, 165, 0), (255, 192, 203), (0, 255, 127),
#             (255, 215, 0), (70, 130, 180), (210, 105, 30), (220, 20, 60), (0, 128, 128),
#             (255, 99, 71)
#         ]

#     def detect_hand(self, image):
#         image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#         results = self.hands.process(image_rgb)
        
#         if results.multi_hand_landmarks:
#             return results.multi_hand_landmarks[0]
#         else:
#             return None

#     def get_hand_info(self, image, hand_landmarks):
#         h, w = image.shape[:2]
#         hand_info = {}

#         wrist = hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]
#         middle_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
#         if wrist.x < middle_mcp.x:
#             hand_info['label'] = "Left Hand"
#         else:
#             hand_info['label'] = "Right Hand"

#         finger_tips = [
#             self.mp_hands.HandLandmark.THUMB_TIP,
#             self.mp_hands.HandLandmark.INDEX_FINGER_TIP,
#             self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
#             self.mp_hands.HandLandmark.RING_FINGER_TIP,
#             self.mp_hands.HandLandmark.PINKY_TIP
#         ]
#         finger_bases = [
#             self.mp_hands.HandLandmark.THUMB_MCP,
#             self.mp_hands.HandLandmark.INDEX_FINGER_MCP,
#             self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP,
#             self.mp_hands.HandLandmark.RING_FINGER_MCP,
#             self.mp_hands.HandLandmark.PINKY_MCP
#         ]

#         if self.prev_landmarks is None:
#             self.prev_landmarks = hand_landmarks
#             self.prev_velocity = [(0, 0) for _ in range(len(hand_landmarks.landmark))]
#         else:
#             for i, landmark in enumerate(hand_landmarks.landmark):
#                 prev_x, prev_y = self.prev_landmarks.landmark[i].x, self.prev_landmarks.landmark[i].y
                
#                 # Вычисляем текущую скорость
#                 current_velocity = (landmark.x - prev_x, landmark.y - prev_y)
                
#                 # Применяем фильтр скорости
#                 filtered_velocity = (
#                     self.velocity_filter * current_velocity[0] + (1 - self.velocity_filter) * self.prev_velocity[i][0],
#                     self.velocity_filter * current_velocity[1] + (1 - self.velocity_filter) * self.prev_velocity[i][1]
#                 )
                
#                 # Обновляем положение с учетом отфильтрованной скорости
#                 landmark.x = prev_x + filtered_velocity[0]
#                 landmark.y = prev_y + filtered_velocity[1]
                
#                 # Применяем дополнительное сглаживание
#                 landmark.x = self.smooth_factor * landmark.x + (1 - self.smooth_factor) * prev_x
#                 landmark.y = self.smooth_factor * landmark.y + (1 - self.smooth_factor) * prev_y
                
#                 # Обновляем предыдущую скорость
#                 self.prev_velocity[i] = filtered_velocity

#         self.prev_landmarks = hand_landmarks

#         hand_info['finger_tips'] = [(int(hand_landmarks.landmark[tip].x * w), int(hand_landmarks.landmark[tip].y * h)) for tip in finger_tips]
#         hand_info['finger_directions'] = [
#             (hand_landmarks.landmark[tip].x - hand_landmarks.landmark[base].x, 
#              hand_landmarks.landmark[tip].y - hand_landmarks.landmark[base].y)
#             for tip, base in zip(finger_tips, finger_bases)
#         ]

#         index_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_MCP]
#         pinky_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_MCP]
#         hand_direction = (pinky_mcp.x - index_mcp.x, pinky_mcp.y - index_mcp.y)
#         hand_info['hand_direction'] = hand_direction

#         return hand_info

#     def draw_hand(self, image, hand_info, hand_landmarks):
#         height, width = image.shape[:2]
        
#         # Сначала рисуем соединения
#         connections = self.mp_hands.HAND_CONNECTIONS
#         for connection in connections:
#             start_idx = connection[0]
#             end_idx = connection[1]
#             start_point = (int(hand_landmarks.landmark[start_idx].x * width),
#                            int(hand_landmarks.landmark[start_idx].y * height))
#             end_point = (int(hand_landmarks.landmark[end_idx].x * width),
#                          int(hand_landmarks.landmark[end_idx].y * height))
#             cv2.line(image, start_point, end_point, (200, 200, 200), 2)
        
#         # Затем рисуем точки поверх соединений
#         for i, landmark in enumerate(hand_landmarks.landmark):
#             px, py = int(landmark.x * width), int(landmark.y * height)
#             cv2.circle(image, (px, py), 5, self.landmark_colors[i % len(self.landmark_colors)], -1)
        
#         # Рисуем кончики пальцев и оси
#         for i, (x, y) in enumerate(hand_info['finger_tips']):
#             cv2.circle(image, (x, y), 8, self.landmark_colors[i], -1)
#             if self.show_axes[self.finger_names[i]]:
#                 self.draw_finger_axes(image, (x, y), hand_info['finger_directions'][i])

#         cv2.putText(image, hand_info['label'], (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

#         return image

#     def draw_finger_axes(self, image, tip, direction):
#         norm = np.sqrt(direction[0]**2 + direction[1]**2)
#         if norm == 0:
#             return
#         direction = (direction[0] / norm, direction[1] / norm)
        
#         ortho = (-direction[1], direction[0])
        
#         cv2.line(image, tip, (int(tip[0] + self.finger_axis_length * direction[0]), 
#                               int(tip[1] + self.finger_axis_length * direction[1])), (200, 200, 200), 2)
#         cv2.line(image, tip, (int(tip[0] + self.finger_axis_length * ortho[0]), 
#                               int(tip[1] + self.finger_axis_length * ortho[1])), (150, 150, 150), 2)
#         cv2.line(image, tip, (int(tip[0] - self.finger_axis_length * 0.5 * (direction[0] + ortho[0])), 
#                               int(tip[1] - self.finger_axis_length * 0.5 * (direction[1] + ortho[1]))), (100, 100, 100), 2)

#     def draw_finger_buttons(self, image):
#         for i, finger in enumerate(self.finger_names):
#             x = self.button_margin + i * (self.button_size[0] + self.button_margin)
#             y = self.image_height - self.button_size[1] - self.button_margin
#             cv2.rectangle(image, (x, y), (x + self.button_size[0], y + self.button_size[1]), (200, 200, 200), -1)
#             text = f"{finger}: {'On' if self.show_axes[finger] else 'Off'}"
#             cv2.putText(image, text, (x + 5, y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

#     def handle_click(self, x, y):
#         for i, finger in enumerate(self.finger_names):
#             button_x = self.button_margin + i * (self.button_size[0] + self.button_margin)
#             button_y = self.image_height - self.button_size[1] - self.button_margin
#             if button_x < x < button_x + self.button_size[0] and button_y < y < button_y + self.button_size[1]:
#                 self.show_axes[finger] = not self.show_axes[finger]
#                 break

import cv2
import mediapipe as mp
import numpy as np

class HandAPI:
    def __init__(self, surface_api):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False, 
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.surface_api = surface_api
        self.finger_axis_length = 50  
        self.image_width = 0
        self.image_height = 0
        self.finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
        self.show_axes = {name: True for name in self.finger_names}
        self.button_size = (100, 30)
        self.button_margin = 10
        
        self.prev_landmarks = None
        self.ema_landmarks = None
        self.alpha_min = 0.3  # Минимальный коэффициент сглаживания
        self.alpha_max = 0.8  # Максимальный коэффициент сглаживания
        self.velocity_threshold = 0.01  # Порог скорости для адаптивного сглаживания
        
        self.clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        self.contrast_alpha = 1.2
        self.contrast_beta = 10

        self.landmark_colors = [
            (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255),
            (0, 255, 255), (128, 0, 0), (0, 128, 0), (0, 0, 128), (128, 128, 0),
            (128, 0, 128), (0, 128, 128), (255, 165, 0), (255, 192, 203), (0, 255, 127),
            (255, 215, 0), (70, 130, 180), (210, 105, 30), (220, 20, 60), (0, 128, 128),
            (255, 99, 71)
        ]

    def detect_hand(self, image):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image_rgb)
        
        if results.multi_hand_landmarks:
            return results.multi_hand_landmarks[0]
        else:
            return None

    def get_hand_info(self, image, hand_landmarks):
        h, w = image.shape[:2]
        hand_info = {}

        wrist = hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]
        middle_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
        if wrist.x < middle_mcp.x:
            hand_info['label'] = "Left Hand"
        else:
            hand_info['label'] = "Right Hand"

        finger_tips = [
            self.mp_hands.HandLandmark.THUMB_TIP,
            self.mp_hands.HandLandmark.INDEX_FINGER_TIP,
            self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
            self.mp_hands.HandLandmark.RING_FINGER_TIP,
            self.mp_hands.HandLandmark.PINKY_TIP
        ]
        finger_bases = [
            self.mp_hands.HandLandmark.THUMB_MCP,
            self.mp_hands.HandLandmark.INDEX_FINGER_MCP,
            self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP,
            self.mp_hands.HandLandmark.RING_FINGER_MCP,
            self.mp_hands.HandLandmark.PINKY_MCP
        ]

        if self.ema_landmarks is None:
            self.ema_landmarks = hand_landmarks
        else:
            for i, landmark in enumerate(hand_landmarks.landmark):
                prev_x, prev_y = self.ema_landmarks.landmark[i].x, self.ema_landmarks.landmark[i].y
                
                # Вычисляем скорость движения
                velocity = np.sqrt((landmark.x - prev_x)**2 + (landmark.y - prev_y)**2)
                
                # Адаптивный коэффициент сглаживания
                alpha = self.alpha_min + (self.alpha_max - self.alpha_min) * min(velocity / self.velocity_threshold, 1.0)
                
                # Применяем EMA
                self.ema_landmarks.landmark[i].x = alpha * landmark.x + (1 - alpha) * prev_x
                self.ema_landmarks.landmark[i].y = alpha * landmark.y + (1 - alpha) * prev_y

        hand_landmarks = self.ema_landmarks

        hand_info['finger_tips'] = [(int(hand_landmarks.landmark[tip].x * w), int(hand_landmarks.landmark[tip].y * h)) for tip in finger_tips]
        hand_info['finger_directions'] = [
            (hand_landmarks.landmark[tip].x - hand_landmarks.landmark[base].x, 
             hand_landmarks.landmark[tip].y - hand_landmarks.landmark[base].y)
            for tip, base in zip(finger_tips, finger_bases)
        ]

        index_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_MCP]
        pinky_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_MCP]
        hand_direction = (pinky_mcp.x - index_mcp.x, pinky_mcp.y - index_mcp.y)
        hand_info['hand_direction'] = hand_direction

        return hand_info

    def draw_hand(self, image, hand_info, hand_landmarks):
        height, width = image.shape[:2]
        
        # Сначала рисуем соединения
        connections = self.mp_hands.HAND_CONNECTIONS
        for connection in connections:
            start_idx = connection[0]
            end_idx = connection[1]
            start_point = (int(hand_landmarks.landmark[start_idx].x * width),
                           int(hand_landmarks.landmark[start_idx].y * height))
            end_point = (int(hand_landmarks.landmark[end_idx].x * width),
                         int(hand_landmarks.landmark[end_idx].y * height))
            cv2.line(image, start_point, end_point, (200, 200, 200), 2)
        
        # Затем рисуем точки поверх соединений
        for i, landmark in enumerate(hand_landmarks.landmark):
            px, py = int(landmark.x * width), int(landmark.y * height)
            cv2.circle(image, (px, py), 5, self.landmark_colors[i % len(self.landmark_colors)], -1)
        
        # Рисуем кончики пальцев и оси
        for i, (x, y) in enumerate(hand_info['finger_tips']):
            cv2.circle(image, (x, y), 8, self.landmark_colors[i], -1)
            if self.show_axes[self.finger_names[i]]:
                self.draw_finger_axes(image, (x, y), hand_info['finger_directions'][i])

        cv2.putText(image, hand_info['label'], (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        return image

    def draw_finger_axes(self, image, tip, direction):
        norm = np.sqrt(direction[0]**2 + direction[1]**2)
        if norm == 0:
            return
        direction = (direction[0] / norm, direction[1] / norm)
        
        ortho = (-direction[1], direction[0])
        
        cv2.line(image, tip, (int(tip[0] + self.finger_axis_length * direction[0]), 
                              int(tip[1] + self.finger_axis_length * direction[1])), (200, 200, 200), 2)
        cv2.line(image, tip, (int(tip[0] + self.finger_axis_length * ortho[0]), 
                              int(tip[1] + self.finger_axis_length * ortho[1])), (150, 150, 150), 2)
        cv2.line(image, tip, (int(tip[0] - self.finger_axis_length * 0.5 * (direction[0] + ortho[0])), 
                              int(tip[1] - self.finger_axis_length * 0.5 * (direction[1] + ortho[1]))), (100, 100, 100), 2)

    def draw_finger_buttons(self, image):
        for i, finger in enumerate(self.finger_names):
            x = self.button_margin + i * (self.button_size[0] + self.button_margin)
            y = self.image_height - self.button_size[1] - self.button_margin
            cv2.rectangle(image, (x, y), (x + self.button_size[0], y + self.button_size[1]), (200, 200, 200), -1)
            text = f"{finger}: {'On' if self.show_axes[finger] else 'Off'}"
            cv2.putText(image, text, (x + 5, y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

    def handle_click(self, x, y):
        for i, finger in enumerate(self.finger_names):
            button_x = self.button_margin + i * (self.button_size[0] + self.button_margin)
            button_y = self.image_height - self.button_size[1] - self.button_margin
            if button_x < x < button_x + self.button_size[0] and button_y < y < button_y + self.button_size[1]:
                self.show_axes[finger] = not self.show_axes[finger]
                break