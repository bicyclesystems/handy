import cv2
import mediapipe as mp
import numpy as np
import time
import pyautogui

class SurfaceAPI:
    def __init__(self, image):
        self.image = image
        self.image_height, self.image_width = image.shape
        self.last_known_surface_info = None

    def detect_horizontal_surface(self, x, y, region_size=200):
        x1 = max(0, x - region_size // 2)
        y1 = max(0, y - region_size // 2)
        x2 = min(self.image_width, x1 + region_size)
        y2 = min(self.image_height, y1 + region_size)
        
        if x1 >= x2 or y1 >= y2:
            return False
        
        region = self.image[y1:y2, x1:x2]
        
        if region.size == 0:
            return False
        
        gradient_x = cv2.Sobel(region, cv2.CV_64F, 1, 0, ksize=3)
        gradient_y = cv2.Sobel(region, cv2.CV_64F, 0, 1, ksize=3)
        
        magnitude = np.sqrt(gradient_x**2 + gradient_y**2)
        angle = np.arctan2(gradient_y, gradient_x) * 180 / np.pi
        
        strong_edges = magnitude > np.percentile(magnitude, 70)
        
        horizontal_count = np.sum((angle[strong_edges] > -10) & (angle[strong_edges] < 10))
        vertical_count = np.sum((angle[strong_edges] > 80) & (angle[strong_edges] < 100))
        
        return horizontal_count > vertical_count

    def analyze_texture(self, x, y, region_size=100):
        x1 = max(0, x - region_size // 2)
        y1 = max(0, y - region_size // 2)
        x2 = min(self.image_width, x1 + region_size)
        y2 = min(self.image_height, y1 + region_size)
        
        if x1 >= x2 or y1 >= y2:
            return "N/A"
        
        region = self.image[y1:y2, x1:x2]
        
        if region.size == 0:
            return "N/A"
        
        glcm = cv2.GaussianBlur(region, (5,5), 0)
        contrast = cv2.Laplacian(glcm, cv2.CV_64F).var()
        
        if contrast > 100:
            return "Rough"
        elif contrast > 50:
            return "Medium"
        else:
            return "Smooth"

    def get_surface_info(self, x, y, finger_raised):
        if 0 <= x < self.image_width and 0 <= y < self.image_height:
            surface = self.detect_horizontal_surface(x, y)
            texture = self.analyze_texture(x, y) if surface else "N/A"
            
            touching_surface = surface
            
            current_info = {"surface": surface, "texture": texture, "touching_surface": touching_surface}
            
            if self.last_known_surface_info is None or finger_raised:
                self.last_known_surface_info = current_info
            elif not surface and self.last_known_surface_info["surface"]:
                return self.last_known_surface_info
            else:
                self.last_known_surface_info = current_info
            
            return current_info
        else:
            return {"surface": False, "texture": "N/A", "touching_surface": False}

class HandAPI:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)

    def detect_hand(self, image):
        results = self.hands.process(image)
        
        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            return hand_landmarks
        else:
            return None

class FingerTracker:
    def __init__(self):
        self.prev_x = None
        self.prev_y = None
        self.movement_threshold = 10
        self.click_threshold = 50
        self.click_time = 0
        self.no_movement_counter = 0
        self.no_movement_threshold = 50
        self.movement_history = []
        self.history_size = 10
        self.screen_width, self.screen_height = pyautogui.size()
        self.sensitivity = 4
        self.last_click_time = 0
        self.click_cooldown = 0.5

    def track_movement(self, x, y):
        movement = "No movement"
        click = False
        cursor_dx, cursor_dy = 0, 0

        if self.prev_x is not None and self.prev_y is not None:
            dx = x - self.prev_x
            dy = y - self.prev_y 

            self.movement_history.append((dx, dy))
            if len(self.movement_history) > self.history_size:
                self.movement_history.pop(0)

            avg_dx = sum(dx for dx, _ in self.movement_history) / len(self.movement_history)
            avg_dy = sum(dy for _, dy in self.movement_history) / len(self.movement_history)

            if abs(avg_dx) > self.movement_threshold or abs(avg_dy) > self.movement_threshold:
                movement = "Horizontal movement"
                self.no_movement_counter = 0
                cursor_dx = avg_dx * self.sensitivity
                cursor_dy = -avg_dy * self.sensitivity 
            elif abs(dy) > self.click_threshold:
                current_time = time.time()
                if current_time - self.last_click_time > self.click_cooldown:
                    click = True
                    self.click_time = current_time
                    self.last_click_time = current_time
            elif abs(avg_dx) < self.movement_threshold / 2 and abs(avg_dy) < self.movement_threshold / 2:
                self.no_movement_counter += 1
                if self.no_movement_counter >= self.no_movement_threshold:
                    movement = "No movement"
            else:
                self.no_movement_counter = 0

        self.prev_x = x
        self.prev_y = y

        return movement, click, cursor_dx, cursor_dy

    def move_cursor(self, dx, dy):
        current_x, current_y = pyautogui.position()
        new_x = max(0, min(self.screen_width, current_x + dx))
        new_y = max(0, min(self.screen_height, current_y + dy))
        pyautogui.moveTo(new_x, new_y)

    def perform_click(self):
        pyautogui.click()

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 20)  # Set frame rate to 20 FPS

surface_api = None
hand_api = HandAPI()
finger_tracker = FingerTracker()

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Failed to get frame from camera")
        continue
    
    image = cv2.flip(image, 1)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    image_rgb = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2RGB)  # Convert back to RGB for MediaPipe
    hand_landmarks = hand_api.detect_hand(image_rgb)

    if hand_landmarks:
        if hand_landmarks.landmark[mp.solutions.hands.HandLandmark.WRIST].x < hand_landmarks.landmark[mp.solutions.hands.HandLandmark.THUMB_TIP].x:
            hand_label = "Left Hand"
        else:
            hand_label = "Right Hand"

        for landmark in hand_landmarks.landmark:
            x = int(landmark.x * gray_image.shape[1])
            y = int(landmark.y * gray_image.shape[0])
            cv2.circle(gray_image, (x, y), 5, (255), -1)

        index_finger_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP]
        wrist = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.WRIST]

        finger_raised = index_finger_tip.y < wrist.y

        x = int(index_finger_tip.x * gray_image.shape[1])
        y = int(index_finger_tip.y * gray_image.shape[0])
        z = index_finger_tip.z

        if not surface_api:
            surface_api = SurfaceAPI(gray_image)
        else:
            surface_api.image = gray_image

        surface_info = surface_api.get_surface_info(x, y, finger_raised)

        movement, click, cursor_dx, cursor_dy = finger_tracker.track_movement(x, y)

        if movement == "Horizontal movement":
            finger_tracker.move_cursor(cursor_dx, cursor_dy)

        if click:
            finger_tracker.perform_click()

        cv2.circle(gray_image, (x, y), 5, (255), -1)
        cv2.putText(gray_image, f"{hand_label}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255), 2)
        cv2.putText(gray_image, f"Surface: {surface_info['surface']}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255), 2)
        cv2.putText(gray_image, f"Texture: {surface_info['texture']}", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (255), 2)
        
        if surface_info['touching_surface']:
            cv2.putText(gray_image, "Finger touching surface", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255), 2)

        cv2.putText(gray_image, movement, (10, 190), cv2.FONT_HERSHEY_SIMPLEX, 1, (255), 2)

        if click or (time.time() - finger_tracker.click_time < 1):
            cv2.putText(gray_image, "Click", (10, 230), cv2.FONT_HERSHEY_SIMPLEX, 1, (255), 2)

        region_size = 200
        cv2.rectangle(gray_image, 
                      (max(0, x - region_size // 2), max(0, y - region_size // 2)),
                      (min(gray_image.shape[1], x + region_size // 2), min(gray_image.shape[0], y + region_size // 2)),
                      (255), 2)
    else:
        cv2.putText(gray_image, "No hand detected", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255), 2)

    cv2.imshow('Hand Tracking', gray_image)
    
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()