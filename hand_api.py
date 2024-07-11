import cv2
import mediapipe as mp
import numpy as np
from coordinate_system import CoordinateSystem

class HandAPI:
    def __init__(self, surface_api):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False, 
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.coordinate_system = CoordinateSystem()
        self.prev_finger_tips = None
        self.surface_api = surface_api

    def detect_hand(self, image):
        results = self.hands.process(image)
        
        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            return hand_landmarks
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
        
        current_finger_tips = [(int(hand_landmarks.landmark[tip].x * w), int(hand_landmarks.landmark[tip].y * h)) for tip in finger_tips]
        
        if self.prev_finger_tips is None:
            self.prev_finger_tips = current_finger_tips
        else:
            alpha = 0.5
            current_finger_tips = [
                (int(alpha * curr[0] + (1 - alpha) * prev[0]), 
                 int(alpha * curr[1] + (1 - alpha) * prev[1]))
                for curr, prev in zip(current_finger_tips, self.prev_finger_tips)
            ]
            self.prev_finger_tips = current_finger_tips

        hand_info['finger_tips'] = current_finger_tips
        hand_info['finger_directions'] = [
            (hand_landmarks.landmark[tip].x - hand_landmarks.landmark[base].x, 
             hand_landmarks.landmark[tip].y - hand_landmarks.landmark[base].y)
            for tip, base in zip(finger_tips, finger_bases)
        ]

        wrist = hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]
        middle_finger_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
        hand_direction = (middle_finger_mcp.x - wrist.x, middle_finger_mcp.y - wrist.y)
        hand_info['hand_direction'] = hand_direction

        index_finger_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        index_finger_x = int(index_finger_tip.x * w)
        index_finger_y = int(index_finger_tip.y * h)

        if self.surface_api.is_surface_locked and self.surface_api.surface_contour is not None:
            M = cv2.moments(self.surface_api.surface_contour)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                
                relative_x = index_finger_x - cX
                relative_y = cY - index_finger_y  
                
                if relative_y <= 100:
                    hand_info['index_finger_on_surface'] = True
                else:
                    hand_info['index_finger_on_surface'] = False
            else:
                hand_info['index_finger_on_surface'] = False
        else:
            hand_info['index_finger_on_surface'] = False

        return hand_info

    def draw_hand(self, image, hand_info):
        height, width = image.shape[:2]
        for x, y in hand_info['finger_tips']:
            cv2.circle(image, (x, y), 5, (255, 255, 255), -1)

        cv2.putText(image, hand_info['label'], (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        text = "Index finger on surface" if hand_info['index_finger_on_surface'] else "Index finger not on surface"
        text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
        text_x = (width - text_size[0]) // 2
        text_y = height - 20

        cv2.putText(image, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, 
                    (0, 255, 0) if hand_info['index_finger_on_surface'] else (0, 0, 255), 2)

        image = self.coordinate_system.draw_hand_axes(image, hand_info)

        return image

    def process_image(self, image):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        hand_landmarks = self.detect_hand(image_rgb)

        if hand_landmarks:
            hand_info = self.get_hand_info(image, hand_landmarks)
            image = self.draw_hand(image, hand_info)
        else:
            cv2.putText(image, "No hand detected", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            self.prev_finger_tips = None

        self.coordinate_system.draw_buttons(image)

        return image

    def handle_click(self, x, y):
        self.coordinate_system.handle_click(x, y)