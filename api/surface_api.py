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
        self.surface_stability_threshold = 2
        self.previous_surface_contour = None
        self.prev_frame = None
        self.is_clicking = False
        self.click_cooldown = 10
        self.click_counter = 0
        
        self.lower_bound_matrix = np.array([30], dtype=np.uint8)
        self.upper_bound_matrix = np.array([30], dtype=np.uint8)

        self.num_rings = 5
        self.closest_ring = None
        self.closest_half = None
        self.rings = []

        self.prev_finger_position = None
        self.prev_palm_size = None
        self.locked_half = None
        self.locked_half_time = None
        self.y_movement_threshold = 10
        self.palm_size_stability_threshold = 0.1
        self.lock_duration = 6.0  
        self.got_it_time = None
        self.crossed_ring = False

    def detect_surface(self, image):
        if self.got_it_time and time.time() - self.got_it_time <= self.lock_duration:
            return

        if self.is_surface_locked:
            return

        height, width = image.shape[:2]
        lower_bound = int(height * 0.4) 

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

                new_surface_contour[:,:,1] += lower_bound

                if self.previous_surface_contour is not None:
                    similarity = cv2.matchShapes(self.previous_surface_contour, new_surface_contour, 1, 0.0)
                    current_time = time.time()

                    if similarity < 0.1: 
                        if self.last_surface_update is None:
                            self.last_surface_update = current_time
                        elif current_time - self.last_surface_update >= self.surface_stability_threshold:
                            self.is_surface_locked = True
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
        self.rings = []

    def update_center(self, finger_position):
        if self.is_surface_locked and self.surface_contour is not None:
            if self.is_point_inside_contour(finger_position): 
                self.center = (finger_position[0], finger_position[1])  
            elif self.center is None: 
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
                cv2.drawContours(overlay, [self.surface_contour], 0, (0, 255, 0), -1)
                cv2.addWeighted(overlay, 0.3, image, 0.7, 0, image)
                cv2.drawContours(image, [self.surface_contour], 0, (0, 255, 0), 2)

                self.draw_inner_rings(image, self.surface_contour)

                if self.is_surface_locked and self.center:
                    self.highlight_closest_ring_half(image, self.center, None)

        self.draw_axes(image)
        
        return image

    def draw_inner_rings(self, image, contour):
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            return

        max_dist = max([cv2.pointPolygonTest(contour, (cX, cY), True) for point in contour[:, 0]])

        self.rings = []
        for i in range(self.num_rings + 1):
            scale = 1 - (i / (self.num_rings + 1))
            scaled_contour = np.array([[(p[0][0] - cX) * scale + cX, (p[0][1] - cY) * scale + cY] for p in contour])
            scaled_contour = scaled_contour.astype(np.int32)
            self.rings.append(scaled_contour)
            cv2.drawContours(image, [scaled_contour], 0, (0, 255, 0), 2)

    def highlight_closest_ring_half(self, image, finger_position, palm_size):
        if not self.rings:
            return

        current_time = time.time()

        if self.got_it_time and current_time - self.got_it_time <= self.lock_duration:
            self.closest_half = self.locked_half
        else:
            if self.prev_finger_position is not None:
                finger_movement = abs(finger_position[1] - self.prev_finger_position[1])
                
                palm_size_change = 0
                if self.prev_palm_size is not None and palm_size is not None and self.prev_palm_size != 0:
                    palm_size_change = abs(palm_size - self.prev_palm_size) / self.prev_palm_size

                if (finger_movement > self.y_movement_threshold and 
                    palm_size_change < self.palm_size_stability_threshold):
                    if self.locked_half is None:
                        self.locked_half = self.closest_half
                        self.locked_half_time = current_time
                        self.got_it_time = current_time 
                        ring_contour = self.rings[self.closest_ring]
                        self.crossed_ring = cv2.pointPolygonTest(ring_contour, finger_position, False) >= 0
                else:
                    if not self.got_it_time or current_time - self.got_it_time > self.lock_duration:
                        self.locked_half = None
                        self.locked_half_time = None
                        self.got_it_time = None
                        self.crossed_ring = False

            if self.locked_half is None:
                distances = [cv2.pointPolygonTest(ring, finger_position, True) for ring in self.rings]
                self.closest_ring = np.argmin(np.abs(distances))

                ring = self.rings[self.closest_ring]
                M = cv2.moments(ring)
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    self.closest_half = "upper" if finger_position[1] < cY else "lower"

        ring = self.rings[self.closest_ring]
        M = cv2.moments(ring)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

        mask = np.zeros(image.shape[:2], dtype=np.uint8)
        cv2.drawContours(mask, [ring], 0, 255, -1)
        if self.closest_half == "upper":
            mask[cY:, :] = 0
        else:
            mask[:cY, :] = 0
        
        red_overlay = np.zeros_like(image)
        red_overlay[mask == 255] = (0, 0, 255)
        
        cv2.addWeighted(image, 1, red_overlay, 0.5, 0, image)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(image, contours, -1, (0, 0, 255), 2)

        if self.got_it_time and current_time - self.got_it_time <= self.lock_duration:
            text = "got it!"
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1
            thickness = 2
            text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
            text_x = (image.shape[1] - text_size[0]) // 2
            text_y = (image.shape[0] + text_size[1]) // 2
            cv2.putText(image, text, (text_x, text_y), font, font_scale, (0, 0, 255), thickness)

            if self.crossed_ring:
                aga_text = "AGA!!!!"
                aga_text_size = cv2.getTextSize(aga_text, font, font_scale, thickness)[0]
                aga_text_x = (image.shape[1] - aga_text_size[0]) // 2
                aga_text_y = text_y + aga_text_size[1] + 10
                cv2.putText(image, aga_text, (aga_text_x, aga_text_y), font, font_scale, (0, 255, 0), thickness)

        self.prev_finger_position = finger_position
        self.prev_palm_size = palm_size

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

    def draw_vertical_axis(self, image):
        if self.center is not None:
            cX, cY = self.center
            cv2.line(image, (cX, cY - 100), (cX, cY + 100), (255, 0, 0), 2)  

    def is_point_inside_contour(self, point):
        if self.surface_contour is None:
            return False
        return cv2.pointPolygonTest(self.surface_contour, point, False) >= 0

    def handle_click(self, x, y):
        if self.surface_contour is not None:
            if self.is_point_inside_contour((x, y)):
                self.is_clicking = True
                self.click_counter = self.click_cooldown

    def update(self, image, finger_position, palm_size):
        if self.got_it_time and time.time() - self.got_it_time <= self.lock_duration:
            self.highlight_closest_ring_half(image, finger_position, palm_size)
            return

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

        if self.is_surface_locked and self.surface_contour is not None:
            self.highlight_closest_ring_half(image, finger_position, palm_size)
        
        self.update_center(finger_position)
        self.prev_frame = image.copy()