import cv2
import mediapipe as mp
import numpy as np

class SurfaceAPI:
    def __init__(self, image):
        self.image = image
        self.image_height, self.image_width, _ = image.shape
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
        
        gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
        
        gradient_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        gradient_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        
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
        
        gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
        glcm = cv2.GaussianBlur(gray, (5,5), 0)
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
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image_rgb)
        
        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            return hand_landmarks
        else:
            return None

cap = cv2.VideoCapture(0)

surface_api = None
hand_api = HandAPI()

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Failed to get frame from camera")
        continue
    
    image = cv2.flip(image, 1)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    hand_landmarks = hand_api.detect_hand(image)

    if hand_landmarks:
        if hand_landmarks.landmark[mp.solutions.hands.HandLandmark.WRIST].x < hand_landmarks.landmark[mp.solutions.hands.HandLandmark.THUMB_TIP].x:
            hand_label = "Left Hand"
        else:
            hand_label = "Right Hand"

        for landmark in hand_landmarks.landmark:
            x = int(landmark.x * image.shape[1])
            y = int(landmark.y * image.shape[0])
            cv2.circle(image, (x, y), 5, (255, 0, 0), -1)

        index_finger_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP]
        wrist = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.WRIST]

        finger_raised = index_finger_tip.y < wrist.y

        x = int(index_finger_tip.x * image.shape[1])
        y = int(index_finger_tip.y * image.shape[0])
        z = index_finger_tip.z

        if not surface_api:
            surface_api = SurfaceAPI(image)
        else:
            surface_api.image = image

        surface_info = surface_api.get_surface_info(x, y, finger_raised)

        cv2.circle(image, (x, y), 5, (0, 255, 0), -1)
        cv2.putText(image, f"{hand_label}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(image, f"Surface: {surface_info['surface']}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(image, f"Texture: {surface_info['texture']}", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        if surface_info['touching_surface']:
            cv2.putText(image, "Finger touching surface", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        region_size = 200
        cv2.rectangle(image, 
                      (max(0, x - region_size // 2), max(0, y - region_size // 2)),
                      (min(image.shape[1], x + region_size // 2), min(image.shape[0], y + region_size // 2)),
                      (255, 0, 0), 2)
    else:
        cv2.putText(image, "No hand detected", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow('Hand Tracking', image)
    
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()