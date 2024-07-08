import cv2
import mediapipe as mp
import numpy as np

class SurfaceAPI:
    def __init__(self, image):
        self.image = image
        self.image_height, self.image_width, _ = image.shape

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
        
        # Compute gradients
        gradient_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        gradient_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        
        # Compute gradient magnitudes and angles
        magnitude = np.sqrt(gradient_x**2 + gradient_y**2)
        angle = np.arctan2(gradient_y, gradient_x) * 180 / np.pi
        
        # Consider only strong edges
        strong_edges = magnitude > np.percentile(magnitude, 70)
        
        # Count horizontal gradients
        horizontal_count = np.sum((angle[strong_edges] > -10) & (angle[strong_edges] < 10))
        vertical_count = np.sum((angle[strong_edges] > 80) & (angle[strong_edges] < 100))
        
        # If there are significantly more horizontal gradients than vertical, it's likely a horizontal surface
        return horizontal_count > 2 * vertical_count

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

    def get_surface_info(self, x, y):
        if 0 <= x < self.image_width and 0 <= y < self.image_height:
            surface = self.detect_horizontal_surface(x, y)
            texture = self.analyze_texture(x, y) if surface else "N/A"
            return {"surface": surface, "texture": texture}
        else:
            return {"surface": False, "texture": "N/A"}

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)

# Initialize video capture
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Failed to get frame from camera")
        continue
    
    image = cv2.flip(image, 1)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    # Create SurfaceAPI instance
    surface_api = SurfaceAPI(image)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            x = int(index_finger_tip.x * image.shape[1])
            y = int(index_finger_tip.y * image.shape[0])
            
            # Get surface info at finger tip
            surface_info = surface_api.get_surface_info(x, y)
            
            cv2.circle(image, (x, y), 5, (0, 255, 0), -1)
            cv2.putText(image, f"Surface: {surface_info['surface']}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(image, f"Texture: {surface_info['texture']}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Draw the analyzed region
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