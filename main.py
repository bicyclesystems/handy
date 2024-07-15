import cv2
import numpy as np
from hand_api import HandAPI
from surface_api import SurfaceAPI
from collections import deque

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 20)

surface_api = SurfaceAPI(highlight_color=(0, 255, 0, 0.05))
hand_api = HandAPI(surface_api)

def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        hand_api.handle_click(x, y)
        surface_api.handle_click(x, y)

cv2.namedWindow('Hand and Surface Tracking')
cv2.setMouseCallback('Hand and Surface Tracking', mouse_callback)

y_history = deque(maxlen=3)
size_history = deque(maxlen=3)
threshold_y = 10
threshold_size = 0.02

current_state = "Initializing"

finger_tips_history = [deque(maxlen=5) for _ in range(5)]

def calculate_hand_size(landmarks):
    points = np.array([(lm.x, lm.y) for lm in landmarks.landmark])
    return np.linalg.norm(points.max(axis=0) - points.min(axis=0))

def smooth_finger_tips(new_tips):
    smoothed_tips = []
    for i, tip in enumerate(new_tips):
        finger_tips_history[i].append(tip)
        avg_tip = np.mean(finger_tips_history[i], axis=0)
        smoothed_tips.append((int(avg_tip[0]), int(avg_tip[1])))
    return smoothed_tips

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Failed to get frame from camera")
        continue
    
    image = cv2.flip(image, 1)
    
    surface_api.detect_surface(image)
    
    hand_landmarks = hand_api.detect_hand(image)
    if hand_landmarks:
        hand_info = hand_api.get_hand_info(image, hand_landmarks)
        
        smoothed_finger_tips = smooth_finger_tips(hand_info['finger_tips'])
        hand_info['finger_tips'] = smoothed_finger_tips
        
        index_finger_tip = hand_info['finger_tips'][1]
        
        current_y = index_finger_tip[1]
        current_size = calculate_hand_size(hand_landmarks)
        
        y_history.append(current_y)
        size_history.append(current_size)
        
        if len(y_history) == y_history.maxlen:
            y_change = max(y_history) - min(y_history)
            
            size_changes = [abs(size_history[i] - size_history[i-1]) / size_history[i-1] for i in range(1, len(size_history))]
            size_changing = any(change > threshold_size for change in size_changes)
            
            if y_change > threshold_y and size_changing:
                current_state = "Y changing, size changing"
            elif y_change > threshold_y:
                current_state = "Y changing, size stable"
            elif size_changing:
                current_state = "Y stable, size changing"
            else:
                current_state = "Hand at rest"
        
        cv2.putText(image, current_state, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        surface_api.update_center(index_finger_tip)
        image = hand_api.draw_hand(image, hand_info)
    else:
        cv2.putText(image, "No hand detected", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        current_state = "Initializing"
        y_history.clear()
        size_history.clear()
        for history in finger_tips_history:
            history.clear()
    
    image = surface_api.highlight_surface(image)
    
    cv2.imshow('Hand and Surface Tracking', image)
    
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()