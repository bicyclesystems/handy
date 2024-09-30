import cv2
import numpy as np
import time

class SurfaceAPI:
    def __init__(self, highlight_color=(200, 200, 200, 0.05)):
        self.surface_color = None
        self.surface_contour = None
        self.highlight_color = highlight_color
        self.is_surface_locked = False
        self.axis_length = 900 
        self.tick_interval = 50 
        self.center = None
        self.surface_level = None
        self.last_surface_update = None
        self.surface_stability_threshold = 2
        self.previous_surface_contour = None
        self.prev_frame = None
        self.is_clicking = False
        self.click_cooldown = 10
        self.click_counter = 0
        
        self.lower_bound_matrix = np.array([30], dtype=np.uint8)
        self.upper_bound_matrix = np.array([30], dtype=np.uint8)

    def detect_surface(self, image):
        if self.is_surface_locked:
            return

        height, width = image.shape[:2]
        lower_bound = int(height * 0.4)  # Начало нижних 60% экрана
        
        # Обрезаем изображение до нижних 60%
        roi = image[lower_bound:, :]

        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(largest_contour)
            if area > 1000: 
                self.surface_color = np.mean(roi[largest_contour[:,:,1], largest_contour[:,:,0]])
                new_surface_contour = largest_contour

                # Смещаем контур обратно на полное изображение
                new_surface_contour[:,:,1] += lower_bound

                if self.previous_surface_contour is not None:
                    similarity = cv2.matchShapes(self.previous_surface_contour, new_surface_contour, 1, 0.0)
                    current_time = time.time()

                    if similarity < 0.1: 
                        if self.last_surface_update is None:
                            self.last_surface_update = current_time
                        elif current_time - self.last_surface_update >= self.surface_stability_threshold:
                            self.is_surface_locked = True
                            print("Surface automatically locked")
                    else:
                        self.last_surface_update = None

                self.surface_contour = new_surface_contour
                self.previous_surface_contour = new_surface_contour
            else:
                self.reset_surface()
        else:
            self.reset_surface()

    def reset_surface(self):
        self.surface_color = None
        self.surface_contour = None
        self.previous_surface_contour = None
        self.last_surface_update = None

    def update_center(self, finger_position):
        if self.is_surface_locked and self.surface_contour is not None:
            if self.center is None:
                M = cv2.moments(self.surface_contour)
                if M["m00"] != 0:
                    self.center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

    def highlight_surface(self, image):
        height, width = image.shape[:2]
        
        if self.surface_color is not None:
            gray_color = int(self.surface_color)
            cv2.rectangle(image, (width-50, height-50), (width-10, height-10), (gray_color, gray_color, gray_color), -1)
            
            if self.surface_contour is not None:
                overlay = image.copy()
                cv2.drawContours(overlay, [self.surface_contour], 0, (200, 200, 200), -1)
                cv2.addWeighted(overlay, 0.3, image, 0.7, 0, image)
                cv2.drawContours(image, [self.surface_contour], 0, (255, 255, 255), 2)
        
        self.draw_axes(image)
        
        return image

    def draw_axes(self, image):
        if self.surface_contour is not None and self.is_surface_locked and self.center is not None:
            cX, cY = self.center

            cv2.line(image, (cX, cY), (cX + self.axis_length, cY), (200, 200, 200), 2) 
            cv2.line(image, (cX, cY), (cX, cY + self.axis_length), (150, 150, 150), 2)  
            cv2.line(image, (cX, cY), (cX, cY - self.axis_length), (100, 100, 100), 2) 

            for i in range(1, self.axis_length // self.tick_interval + 1):
                tick_length = 10
                tick_value = i * self.tick_interval
                
                x_tick = cX + i * self.tick_interval
                cv2.line(image, (x_tick, cY - tick_length), (x_tick, cY + tick_length), (200, 200, 200), 1)
                cv2.putText(image, str(tick_value), (x_tick - 10, cY + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
                
                y_tick = cY + i * self.tick_interval
                cv2.line(image, (cX - tick_length, y_tick), (cX + tick_length, y_tick), (150, 150, 150), 1)
                cv2.putText(image, str(tick_value), (cX - 40, y_tick + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150, 150, 150), 1)
                
                z_tick = cY - i * self.tick_interval
                cv2.line(image, (cX - tick_length, z_tick), (cX + tick_length, z_tick), (100, 100, 100), 1)
                cv2.putText(image, str(tick_value), (cX + 15, z_tick + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 100, 100), 1)

            cv2.putText(image, "X", (cX + self.axis_length + 10, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2)
            cv2.putText(image, "Y", (cX, cY + self.axis_length + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (150, 150, 150), 2)
            cv2.putText(image, "Z", (cX, cY - self.axis_length - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 100, 100), 2)

    def is_point_inside_contour(self, point):
        if self.surface_contour is None:
            return False
        return cv2.pointPolygonTest(self.surface_contour, point, False) >= 0

    def handle_click(self, x, y):
        if self.surface_contour is not None:
            if self.is_point_inside_contour((x, y)):
                self.is_clicking = True
                self.click_counter = self.click_cooldown
                print(f"Click detected at ({x}, {y})")

    def update(self, image):
        if self.is_clicking:
            self.click_counter -= 1
            if self.click_counter <= 0:
                self.is_clicking = False

        if not self.is_clicking and self.is_surface_locked:
            if self.prev_frame is not None:
                diff = cv2.absdiff(image, self.prev_frame)
                mean_diff = np.mean(diff)
                if mean_diff > 30: 
                    self.is_surface_locked = False
                    print("Surface automatically unlocked due to significant changes")

        self.prev_frame = image.copy()