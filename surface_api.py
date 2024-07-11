import cv2
import numpy as np

class SurfaceAPI:
    def __init__(self, highlight_color=(0, 255, 0, 0.05)):
        self.surface_color = None
        self.surface_contour = None
        self.highlight_color = highlight_color
        self.is_surface_locked = False
        self.lock_button_size = (200, 50)
        self.axis_length = 900 
        self.tick_interval = 50 
        self.center = None  

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
            self.surface_contour = best_contour
            self.surface_contour[:,:,1] += height // 2
        else:
            self.surface_color = None
            self.surface_contour = None

    def highlight_surface(self, image):
        height, width = image.shape[:2]
        
        if self.surface_color is not None:
            cv2.rectangle(image, (width-50, height-50), (width-10, height-10), self.surface_color.tolist(), -1)
            
            if self.surface_contour is not None:
                overlay = image.copy()
                cv2.drawContours(overlay, [self.surface_contour], 0, self.highlight_color[:3], -1)
                cv2.addWeighted(overlay, self.highlight_color[3], image, 1 - self.highlight_color[3], 0, image)
                cv2.drawContours(image, [self.surface_contour], 0, self.highlight_color[:3], 2)
        
        self.lock_button_pos = (width - self.lock_button_size[0] - 10, 10)
        self.draw_lock_button(image)
        
        self.draw_axes(image)
        
        return image

    def draw_lock_button(self, image):
        x, y = self.lock_button_pos
        w, h = self.lock_button_size
        cv2.rectangle(image, (x, y), (x + w, y + h), (200, 200, 200), -1)
        text = "Unlock Surface" if self.is_surface_locked else "Lock Surface"
        cv2.putText(image, text, (x + 10, y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

    def handle_click(self, x, y):
        if self.is_mouse_over_button((x, y), self.lock_button_pos, self.lock_button_size):
            self.is_surface_locked = not self.is_surface_locked

    def is_mouse_over_button(self, mouse_pos, button_pos, button_size):
        return (button_pos[0] < mouse_pos[0] < button_pos[0] + button_size[0] and
                button_pos[1] < mouse_pos[1] < button_pos[1] + button_size[1])

    def draw_axes(self, image):
        if self.surface_contour is not None and self.is_surface_locked and self.center is not None:
            cX, cY = self.center

            cv2.line(image, (cX, cY), (cX + self.axis_length, cY), (0, 0, 255), 2)
            
            cv2.line(image, (cX, cY), (cX - self.axis_length // 2, cY - self.axis_length // 2), (0, 255, 0), 2)
            
            cv2.line(image, (cX, cY), (cX, cY - self.axis_length), (255, 0, 0), 2)

            for i in range(1, self.axis_length // self.tick_interval + 1):
                tick_length = 10
                tick_value = i * self.tick_interval
                
                x_tick = cX + i * self.tick_interval
                cv2.line(image, (x_tick, cY - tick_length), (x_tick, cY + tick_length), (0, 0, 255), 1)
                cv2.putText(image, str(tick_value), (x_tick - 10, cY + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                
                y_tick_x = cX - (i * self.tick_interval) // 2
                y_tick_y = cY - (i * self.tick_interval) // 2
                cv2.line(image, (y_tick_x - tick_length, y_tick_y), (y_tick_x + tick_length, y_tick_y), (0, 255, 0), 1)
                cv2.putText(image, str(tick_value), (y_tick_x - 30, y_tick_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                
                z_tick = cY - i * self.tick_interval
                cv2.line(image, (cX - tick_length, z_tick), (cX + tick_length, z_tick), (255, 0, 0), 1)
                cv2.putText(image, str(tick_value), (cX + 15, z_tick + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

            cv2.putText(image, "X", (cX + self.axis_length + 10, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(image, "Y", (cX - self.axis_length // 2 - 30, cY - self.axis_length // 2 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(image, "Z", (cX, cY - self.axis_length - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

    def update_center(self, new_center):
        self.center = new_center