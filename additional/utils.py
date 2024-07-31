import cv2
import numpy as np

def calculate_hand_size(landmarks):
    points = np.array([(lm.x, lm.y) for lm in landmarks.landmark])
    return np.linalg.norm(points.max(axis=0) - points.min(axis=0))

def smooth_finger_tips(new_tips, finger_tips_history):
    smoothed_tips = []
    for i, tip in enumerate(new_tips):
        finger_tips_history[i].append(tip)
        avg_tip = np.mean(finger_tips_history[i], axis=0)
        smoothed_tips.append((int(avg_tip[0]), int(avg_tip[1])))
    return smoothed_tips

def update_state(new_state, state_transition, state_transition_threshold):
    for state in state_transition:
        if state == new_state:
            state_transition[state] += 1
        else:
            state_transition[state] = max(0, state_transition[state] - 1)
    
    if state_transition[new_state] >= state_transition_threshold:
        return new_state
    return None

def draw_size_change_graph(image, size_changes):
    graph_height = 150
    graph_width = 300
    graph = np.zeros((graph_height, graph_width, 3), dtype=np.uint8)
    for i, change in enumerate(size_changes):
        y = int((1 - change) * (graph_height - 1))
        cv2.circle(graph, (i * 2, y), 1, (0, 255, 0), -1)
    
    image[10:10+graph_height, -graph_width-10:-10] = graph
    return image

def calculate_hand_center(landmarks, width, height):
    points = np.array([(lm.x * width, lm.y * height) for lm in landmarks.landmark])
    return np.mean(points, axis=0)

def detect_significant_changes(current_frame, prev_frame, change_threshold):
    if prev_frame is None:
        return False
    
    diff = cv2.absdiff(current_frame, prev_frame)
    gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray_diff, 25, 255, cv2.THRESH_BINARY)
    change_percent = (np.sum(threshold) / 255) / (threshold.shape[0] * threshold.shape[1]) * 100
    
    return change_percent > change_threshold

def setup_window(mouse_callback):
    cv2.namedWindow('Hand and Surface Tracking')
    cv2.setMouseCallback('Hand and Surface Tracking', mouse_callback)