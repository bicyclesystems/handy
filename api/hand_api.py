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
            min_tracking_confidence=0.5,
            model_complexity=1
        )
        self.surface_api = surface_api
        self.finger_axis_length = 50  
        self.image_width = 0
        self.image_height = 0
        self.finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
        self.show_axes = {name: True for name in self.finger_names}
        self.button_size = (100, 30)
        self.button_margin = 10
        
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

        self.smoothed_landmarks = None
        self.alpha_min = 0.3
        self.alpha_max = 0.8
        self.velocity_threshold = 0.005

        self.depth_threshold = 0.03
        self.perpendicular_adjustment = 2.5
        self.finger_length_threshold = 0.08

        self.smoothing_factor = 0.5  # New smoothing factor

    def preprocess_image(self, image):
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        l = self.clahe.apply(l)
        lab = cv2.merge((l, a, b))
        image = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        
        gamma = 1.5
        lookup_table = np.array([((i / 255.0) ** (1.0 / gamma)) * 255 for i in np.arange(0, 256)]).astype("uint8")
        image = cv2.LUT(image, lookup_table)
        
        return image

    def detect_hand(self, image):
        preprocessed_image = self.preprocess_image(image)
        image_rgb = cv2.cvtColor(preprocessed_image, cv2.COLOR_BGR2RGB)
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

        current_landmarks = np.array([[landmark.x, landmark.y, landmark.z] for landmark in hand_landmarks.landmark])
        
        if self.smoothed_landmarks is None:
            self.smoothed_landmarks = current_landmarks
        else:
            # Уменьшаем эффект сглаживания
            self.smoothed_landmarks = self.smoothing_factor * self.smoothed_landmarks + (1 - self.smoothing_factor) * current_landmarks

        for i, smoothed in enumerate(self.smoothed_landmarks):
            hand_landmarks.landmark[i].x = smoothed[0]
            hand_landmarks.landmark[i].y = smoothed[1]
            hand_landmarks.landmark[i].z = smoothed[2]

        hand_info['finger_tips'] = []
        hand_info['finger_directions'] = []
        hand_info['is_perpendicular'] = []
        hand_info['is_finger_bent'] = []

        for tip, base in zip(finger_tips, finger_bases):
            tip_landmark = hand_landmarks.landmark[tip]
            base_landmark = hand_landmarks.landmark[base]
            
            direction = (
                tip_landmark.x - base_landmark.x,
                tip_landmark.y - base_landmark.y,
                tip_landmark.z - base_landmark.z
            )
            
            finger_length = np.sqrt(direction[0]**2 + direction[1]**2 + direction[2]**2)
            is_finger_bent = finger_length < self.finger_length_threshold
            
            norm = np.sqrt(direction[0]**2 + direction[1]**2 + direction[2]**2)
            if norm != 0:
                direction = tuple(d / norm for d in direction)
            
            is_perpendicular = abs(direction[2]) > self.depth_threshold or is_finger_bent
            
            hand_info['finger_tips'].append((int(tip_landmark.x * w), int(tip_landmark.y * h)))
            hand_info['finger_directions'].append(direction)
            hand_info['is_perpendicular'].append(is_perpendicular)
            hand_info['is_finger_bent'].append(is_finger_bent)

        index_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_MCP]
        pinky_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_MCP]
        hand_direction = (pinky_mcp.x - index_mcp.x, pinky_mcp.y - index_mcp.y, pinky_mcp.z - index_mcp.z)
        hand_info['hand_direction'] = hand_direction

        hand_info['landmark_depths'] = [landmark.z for landmark in hand_landmarks.landmark]

        return hand_info

    def draw_hand(self, image, hand_info, hand_landmarks):
        height, width = image.shape[:2]
        
        connections = self.mp_hands.HAND_CONNECTIONS
        for connection in connections:
            start_idx = connection[0]
            end_idx = connection[1]
            start_point = (int(hand_landmarks.landmark[start_idx].x * width),
                           int(hand_landmarks.landmark[start_idx].y * height))
            end_point = (int(hand_landmarks.landmark[end_idx].x * width),
                         int(hand_landmarks.landmark[end_idx].y * height))
            cv2.line(image, start_point, end_point, (200, 200, 200), 2)
        
        for i, landmark in enumerate(hand_landmarks.landmark):
            px, py = int(landmark.x * width), int(landmark.y * height)
            depth = hand_info['landmark_depths'][i]
            color = self.get_depth_color(depth)
            cv2.circle(image, (px, py), 5, color, -1)
        
        for i, ((x, y), is_perpendicular, is_bent) in enumerate(zip(hand_info['finger_tips'], hand_info['is_perpendicular'], hand_info['is_finger_bent'])):
            radius = 8 * (self.perpendicular_adjustment if is_perpendicular else 1)
            color = (0, 0, 255) if is_bent else self.landmark_colors[i]
            cv2.circle(image, (x, y), int(radius), color, -1)
            if self.show_axes[self.finger_names[i]]:
                self.draw_finger_axes(image, (x, y), hand_info['finger_directions'][i])

        cv2.putText(image, hand_info['label'], (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        return image

    def get_depth_color(self, depth):
        normalized_depth = (depth + 0.5) / 1.0
        normalized_depth = max(0, min(1, normalized_depth))
        
        r = int(255 * normalized_depth)
        b = int(255 * (1 - normalized_depth))
        return (b, 0, r)

    def draw_finger_axes(self, image, tip, direction):
        norm = np.sqrt(direction[0]**2 + direction[1]**2 + direction[2]**2)
        if norm == 0:
            return
        direction = (direction[0] / norm, direction[1] / norm, direction[2] / norm)
        
        ortho = (-direction[1], direction[0], 0)
        
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