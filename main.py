import cv2
import numpy as np
from hand_api import HandAPI
from surface_api import SurfaceAPI
from collections import deque
import pyautogui

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 20)

_, image = cap.read()
height, width = image.shape[:2]

surface_api = SurfaceAPI(highlight_color=(0, 255, 0, 0.05))
hand_api = HandAPI(surface_api)

hand_api.image_width = width
hand_api.image_height = height

screen_width, screen_height = pyautogui.size()
last_x, last_y = None, None
cursor_sensitivity = 3.0  
smoothing_factor = 0.2
smooth_x, smooth_y = 0, 0

last_cursor_position = None
hand_was_on_surface = False

def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        hand_api.handle_click(x, y)
        surface_api.handle_click(x, y)

cv2.namedWindow('Hand and Surface Tracking')
cv2.setMouseCallback('Hand and Surface Tracking', mouse_callback)

y_history = deque(maxlen=10)
size_history = deque(maxlen=10)
threshold_y = 30
threshold_size = 0.04

current_state = "Initializing"
state_transition = {"Initializing": 0, "Hand at rest": 0, "Y changing, size stable": 0, "Y stable, size changing": 0, "Y changing, size changing": 0}
state_transition_threshold = 3

finger_tips_history = [deque(maxlen=2) for _ in range(5)]

graph_height = 150 
graph_width = 300  
size_change_history = deque(maxlen=150) 

click_state = "up"
click_cooldown = 0
click_cooldown_threshold = 1

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

def update_state(new_state):
    global current_state
    for state in state_transition:
        if state == new_state:
            state_transition[state] += 1
        else:
            state_transition[state] = max(0, state_transition[state] - 1)
    
    if state_transition[new_state] >= state_transition_threshold:
        current_state = new_state

def draw_size_change_graph(image, size_changes):
    graph = np.zeros((graph_height, graph_width, 3), dtype=np.uint8)
    for i, change in enumerate(size_changes):
        y = int((1 - change) * (graph_height - 1))
        cv2.circle(graph, (i * 2, y), 1, (0, 255, 0), -1)
    
    image[10:10+graph_height, -graph_width-10:-10] = graph
    return image

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Failed to get frame from camera")
        continue
    
    image = cv2.flip(image, 1)
    
    if not surface_api.is_surface_locked:
        surface_api.detect_surface(image)
    
    hand_landmarks = hand_api.detect_hand(image)
    if hand_landmarks:
        hand_info = hand_api.get_hand_info(image, hand_landmarks)
        
        smoothed_finger_tips = smooth_finger_tips(hand_info['finger_tips'])
        hand_info['finger_tips'] = smoothed_finger_tips
        
        index_finger_tip = hand_info['finger_tips'][1]
        
        hand_on_surface = surface_api.is_point_inside_contour(index_finger_tip)
        hand_status = "On surface" if hand_on_surface else "Off surface"
        cv2.putText(image, f"Hand: {hand_status}", (10, 180), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        if hand_on_surface and surface_api.is_surface_locked:
            if not hand_was_on_surface:
                if last_cursor_position is not None:
                    pyautogui.moveTo(*last_cursor_position)
                    last_x, last_y = index_finger_tip
                hand_was_on_surface = True
            
            current_y = index_finger_tip[1]
            current_size = calculate_hand_size(hand_landmarks)
            
            y_history.append(current_y)
            size_history.append(current_size)
            
            if len(y_history) == y_history.maxlen:
                y_change = max(y_history) - min(y_history)
                
                size_changes = [abs(size_history[i] - size_history[i-1]) / size_history[i-1] for i in range(1, len(size_history))]
                size_changing = any(change > threshold_size for change in size_changes)
                
                size_change_history.append(size_changes[-1])
                
                new_state = "Hand at rest"
                if y_change > threshold_y and not size_changing:
                    new_state = "Y changing, size stable"
                    
                    if click_state == "up" and current_y > y_history[0]:
                        click_state = "down"
                        print("Click started")
                    elif click_state == "down" and current_y < y_history[0] and click_cooldown == 0:
                        click_state = "up"
                        print("Click finished")
                        pyautogui.click()
                        click_cooldown = click_cooldown_threshold
                
                elif y_change > threshold_y and size_changing:
                    new_state = "Y changing, size changing"
                    if last_x is not None and last_y is not None:
                        dx = (index_finger_tip[0] - last_x) * cursor_sensitivity
                        dy = (last_y - index_finger_tip[1]) * cursor_sensitivity 
                        
                        smooth_x = smoothing_factor * dx + (1 - smoothing_factor) * smooth_x
                        smooth_y = smoothing_factor * dy + (1 - smoothing_factor) * smooth_y
                        
                        current_x, current_y = pyautogui.position()
                        new_x = max(0, min(screen_width, current_x + smooth_x))
                        new_y = max(0, min(screen_height, current_y + smooth_y))
                        pyautogui.moveTo(new_x, new_y)
                        
                        last_cursor_position = (new_x, new_y)
                elif size_changing:
                    new_state = "Y stable, size changing"
                
                last_x, last_y = index_finger_tip
                
                update_state(new_state)
            
            if click_cooldown > 0:
                click_cooldown -= 1
            
            cv2.putText(image, current_state, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(image, f"Click state: {click_state}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            cursor_x, cursor_y = pyautogui.position()
            cv2.putText(image, f"Cursor: ({cursor_x}, {cursor_y})", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            image = draw_size_change_graph(image, size_change_history)
        else:
            current_state = "Hand off surface"
            click_state = "up"
            y_history.clear()
            size_history.clear()
            last_x, last_y = None, None
            hand_was_on_surface = False
        
        surface_api.update_center(index_finger_tip)
        image = hand_api.draw_hand(image, hand_info, hand_landmarks)
        
    else:
        cv2.putText(image, "No hand detected", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        update_state("Initializing")
        y_history.clear()
        size_history.clear()
        size_change_history.clear()
        for history in finger_tips_history:
            history.clear()
        hand_was_on_surface = False
    
    image = surface_api.highlight_surface(image)
    
    hand_api.draw_finger_buttons(image)
    
    lock_status = "Locked" if surface_api.is_surface_locked else "Unlocked"
    cv2.putText(image, f"Surface: {lock_status}", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    cv2.imshow('Hand and Surface Tracking', image)
    
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()