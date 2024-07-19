import cv2
import numpy as np
import time

class SurfaceAPI:
    def __init__(self, highlight_color=(0, 255, 0, 0.05)):
        self.surface_color = None
        self.surface_contour = None
        self.highlight_color = highlight_color
        self.is_surface_locked = False
        self.axis_length = 900 
        self.tick_interval = 50 
        self.center = None
        self.surface_level = None
        self.last_surface_update = None
        self.surface_stability_threshold = 2  # 2 seconds
        self.previous_surface_contour = None

    def detect_surface(self, image):
        if self.is_surface_locked:
            return

        height, width = image.shape[:2]
        lower_half = image[height//2:, :]
        
        hsv = cv2.cvtColor(lower_half, cv2.COLOR_BGR2HSV)
        cell_height = height // 10
        cell_width = width // 10
        
        best_homogeneity = 0
        best_color = None
        best_contour = None
        
        for i in range(5):  
            for j in range(10):
                cell = hsv[i*cell_height:(i+1)*cell_height, j*cell_width:(j+1)*cell_width]
                color_std = np.std(cell, axis=(0,1))
                if np.all(color_std < 20):  
                    mean_color = np.mean(cell, axis=(0,1)).astype(np.uint8)
                    if mean_color[1] < 30:  
                        lower_bound = np.array([0, 0, max(0, mean_color[2]-30)], dtype=np.uint8)
                        upper_bound = np.array([180, 30, min(255, mean_color[2]+30)], dtype=np.uint8)
                    else:
                        lower_bound = np.array([max(0, mean_color[0]-10), max(0, mean_color[1]-50), max(0, mean_color[2]-50)], dtype=np.uint8)
                        upper_bound = np.array([min(180, mean_color[0]+10), min(255, mean_color[1]+50), min(255, mean_color[2]+50)], dtype=np.uint8)
                    
                    mask = cv2.inRange(hsv, lower_bound, upper_bound)
                    
                    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    if contours:
                        largest_contour = max(contours, key=cv2.contourArea)
                        area = cv2.contourArea(largest_contour)
                        if area > best_homogeneity:
                            best_homogeneity = area
                            best_color = cv2.cvtColor(np.uint8([[mean_color]]), cv2.COLOR_HSV2BGR)[0][0]
                            best_contour = largest_contour
        
        if best_color is not None:
            self.surface_color = best_color
            new_surface_contour = best_contour
            new_surface_contour[:,:,1] += height // 2

            if self.previous_surface_contour is not None:
                similarity = cv2.matchShapes(self.previous_surface_contour, new_surface_contour, 1, 0.0)
                current_time = time.time()

                if similarity < 0.1:  # Поверхность считается стабильной
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
            cv2.rectangle(image, (width-50, height-50), (width-10, height-10), self.surface_color.tolist(), -1)
            
            if self.surface_contour is not None:
                overlay = image.copy()
                cv2.drawContours(overlay, [self.surface_contour], 0, self.highlight_color[:3], -1)
                cv2.addWeighted(overlay, self.highlight_color[3], image, 1 - self.highlight_color[3], 0, image)
                cv2.drawContours(image, [self.surface_contour], 0, self.highlight_color[:3], 2)
        
        self.draw_axes(image)
        
        return image

    def draw_axes(self, image):
        if self.surface_contour is not None and self.is_surface_locked and self.center is not None:
            cX, cY = self.center

            cv2.line(image, (cX, cY), (cX + self.axis_length, cY), (0, 0, 255), 2) 
            cv2.line(image, (cX, cY), (cX, cY + self.axis_length), (0, 255, 0), 2)  
            cv2.line(image, (cX, cY), (cX, cY - self.axis_length), (255, 0, 0), 2) 

            for i in range(1, self.axis_length // self.tick_interval + 1):
                tick_length = 10
                tick_value = i * self.tick_interval
                
                x_tick = cX + i * self.tick_interval
                cv2.line(image, (x_tick, cY - tick_length), (x_tick, cY + tick_length), (0, 0, 255), 1)
                cv2.putText(image, str(tick_value), (x_tick - 10, cY + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                
                y_tick = cY + i * self.tick_interval
                cv2.line(image, (cX - tick_length, y_tick), (cX + tick_length, y_tick), (0, 255, 0), 1)
                cv2.putText(image, str(tick_value), (cX - 40, y_tick + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                
                z_tick = cY - i * self.tick_interval
                cv2.line(image, (cX - tick_length, z_tick), (cX + tick_length, z_tick), (255, 0, 0), 1)
                cv2.putText(image, str(tick_value), (cX + 15, z_tick + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

            cv2.putText(image, "X", (cX + self.axis_length + 10, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(image, "Y", (cX, cY + self.axis_length + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(image, "Z", (cX, cY - self.axis_length - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

    def is_point_inside_contour(self, point):
        if self.surface_contour is None:
            return False
        return cv2.pointPolygonTest(self.surface_contour, point, False) >= 0