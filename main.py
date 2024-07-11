import cv2
from hand_api import HandAPI
from surface_api import SurfaceAPI

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
        index_finger_tip = hand_info['finger_tips'][1] 
        surface_api.update_center(index_finger_tip)
        image = hand_api.draw_hand(image, hand_info)
    else:
        cv2.putText(image, "No hand detected", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    image = surface_api.highlight_surface(image)
    
    cv2.imshow('Hand and Surface Tracking', image)
    
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()