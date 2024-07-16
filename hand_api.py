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

        if hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST].x < hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP].x:
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
            self.mp_hands.HandLandmark.THUMB_CMC,
            self.mp_hands.HandLandmark.INDEX_FINGER_MCP,
            self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP,
            self.mp_hands.HandLandmark.RING_FINGER_MCP,
            self.mp_hands.HandLandmark.PINKY_MCP
        ]
        
        hand_info['finger_tips'] = [(int(hand_landmarks.landmark[tip].x * w), int(hand_landmarks.landmark[tip].y * h)) for tip in finger_tips]
        hand_info['finger_directions'] = [
            (hand_landmarks.landmark[tip].x - hand_landmarks.landmark[base].x, 
             hand_landmarks.landmark[tip].y - hand_landmarks.landmark[base].y)
            for tip, base in zip(finger_tips, finger_bases)
        ]

        wrist = hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]
        middle_finger_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
        hand_direction = (middle_finger_mcp.x - wrist.x, middle_finger_mcp.y - wrist.y)
        hand_info['hand_direction'] = hand_direction

        return hand_info

    def draw_hand(self, image, hand_info, hand_landmarks):
        height, width = image.shape[:2]
        for i, (x, y) in enumerate(hand_info['finger_tips']):
            cv2.circle(image, (x, y), 5, (255, 255, 255), -1)
            if self.show_axes[self.finger_names[i]]:
                self.draw_finger_axes(image, (x, y), hand_info['finger_directions'][i])
        
        for landmark in hand_landmarks.landmark:
            px, py = int(landmark.x * width), int(landmark.y * height)
            cv2.circle(image, (px, py), 5, (255, 0, 0), -1)

        cv2.putText(image, hand_info['label'], (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        return image

    def draw_finger_axes(self, image, tip, direction):
        norm = np.sqrt(direction[0]**2 + direction[1]**2)
        if norm == 0:
            return
        direction = (direction[0] / norm, direction[1] / norm)
        
        ortho = (-direction[1], direction[0])
        
        cv2.line(image, tip, (int(tip[0] + self.finger_axis_length * direction[0]), 
                              int(tip[1] + self.finger_axis_length * direction[1])), (0, 0, 255), 2)
        cv2.line(image, tip, (int(tip[0] + self.finger_axis_length * ortho[0]), 
                              int(tip[1] + self.finger_axis_length * ortho[1])), (0, 255, 0), 2)
        cv2.line(image, tip, (int(tip[0] - self.finger_axis_length * 0.5 * (direction[0] + ortho[0])), 
                              int(tip[1] - self.finger_axis_length * 0.5 * (direction[1] + ortho[1]))), (255, 0, 0), 2)

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
