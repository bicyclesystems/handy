import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)

cap = cv2.VideoCapture(0)

screen_width, screen_height = pyautogui.size()

capture_area = {"top": 0.8, "bottom": 1.0, "left": 0.2, "right": 0.8}

buffer_size = 5
x_buffer = []
y_buffer = []

movement_threshold = 5
stationary_time_threshold = 0.5
last_significant_move_time = time.time()
last_position = None

def map_to_screen(x, y, capture_area, image_width, image_height, screen_width, screen_height):
    norm_x = (x - capture_area["left"] * image_width) / ((capture_area["right"] - capture_area["left"]) * image_width)
    norm_y = (y - capture_area["top"] * image_height) / ((capture_area["bottom"] - capture_area["top"]) * image_height)
    norm_x = max(0, min(norm_x, 1))
    norm_y = max(0, min(norm_y, 1))
    screen_x = int(norm_x * screen_width)
    screen_y = int((1 - norm_y) * screen_height)
    return screen_x, screen_y

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Не удалось получить кадр с камеры.")
        continue
    
    image = cv2.flip(image, 1)
    image_height, image_width, _ = image.shape
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            x = int(index_finger_tip.x * image_width)
            y = int(index_finger_tip.y * image_height)

            if (capture_area["left"] * image_width - 10 <= x <= capture_area["right"] * image_width + 10 and
                capture_area["top"] * image_height - 10 <= y <= capture_area["bottom"] * image_height + 10):
                
                screen_x, screen_y = map_to_screen(x, y, capture_area, image_width, image_height, screen_width, screen_height)
                x_buffer.append(screen_x)
                y_buffer.append(screen_y)
                if len(x_buffer) > buffer_size:
                    x_buffer.pop(0)
                    y_buffer.pop(0)
                avg_x = int(np.mean(x_buffer))
                avg_y = int(np.mean(y_buffer))

                current_time = time.time()
                if last_position is None:
                    last_position = (avg_x, avg_y)
                    last_significant_move_time = current_time
                    pyautogui.moveTo(avg_x, avg_y)
                else:
                    distance = np.sqrt((avg_x - last_position[0])**2 + (avg_y - last_position[1])**2)
                    if distance > movement_threshold:
                        last_position = (avg_x, avg_y)
                        last_significant_move_time = current_time
                        pyautogui.moveTo(avg_x, avg_y)
                    elif current_time - last_significant_move_time > stationary_time_threshold:
                        pass
                    else:
                        pyautogui.moveTo(avg_x, avg_y)

    cv2.rectangle(image, 
                  (int(capture_area["left"] * image_width), int(capture_area["top"] * image_height)),
                  (int(capture_area["right"] * image_width), int(capture_area["bottom"] * image_height)),
                  (0, 255, 0), 2)
    
    cv2.imshow('Hand Tracking', image)
    
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()