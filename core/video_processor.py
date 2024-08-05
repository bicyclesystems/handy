import cv2
import pyautogui
import numpy as np
from api import HandAPI, SurfaceAPI
from additional.utils import detect_significant_changes

class VideoProcessor:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FPS, 60)
        _, image = self.cap.read()
        self.height, self.width = image.shape[:2]
        self.screen_size = pyautogui.size()
        
        self.surface_api = SurfaceAPI(highlight_color=(200, 200, 200, 0.05))
        self.hand_api = HandAPI(self.surface_api)
        self.hand_api.image_width = self.width
        self.hand_api.image_height = self.height
        
        self.prev_frame = None
        self.change_threshold = 30

        self.flip_matrix = np.array([[-1, 0, self.width - 1], [0, 1, 0]], dtype=np.float32)

    def is_camera_opened(self):
        return self.cap.isOpened()

    def process_frame(self):
        success, image = self.cap.read()
        if not success:
            print("Failed to get frame from camera")
            return None

        image = cv2.warpAffine(image, self.flip_matrix, (self.width, self.height))

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        
        if detect_significant_changes(image, self.prev_frame, self.change_threshold):
            if self.surface_api.is_surface_locked:
                self.surface_api.is_surface_locked = False
                print("Significant changes detected. Surface unlocked.")
        
        self.prev_frame = image.copy()
        
        if not self.surface_api.is_surface_locked:
            self.surface_api.detect_surface(image)
        
        return image

    def detect_hand(self, image):
        return self.hand_api.detect_hand(image)

    def draw_interface(self, image, state_manager, click_handler):
        image = self.surface_api.highlight_surface(image)
        self.hand_api.draw_finger_buttons(image)
        
        lock_status = "Locked" if self.surface_api.is_surface_locked else "Unlocked"
        cv2.putText(image, f"Surface: {lock_status}", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        cv2.putText(image, state_manager.current_state, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(image, f"Click state: {click_handler.click_state}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        cursor_x, cursor_y = pyautogui.position()
        cv2.putText(image, f"Cursor: ({cursor_x}, {cursor_y})", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        cv2.imshow('Hand and Surface Tracking', image)

    def draw_no_hand_message(self, image):
        cv2.putText(image, "No hand detected", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    def draw_hand_status(self, image, hand_status):
        cv2.putText(image, f"Hand: {hand_status}", (10, 180), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    def should_exit(self):
        return cv2.waitKey(5) & 0xFF == 27

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()

    def mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.hand_api.handle_click(x, y)
            self.surface_api.handle_click(x, y)