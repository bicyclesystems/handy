import cv2
import numpy as np

class SurfaceAPI:
    def __init__(self, highlight_color=(0, 255, 0)):
        self.surface_color = None
        self.surface_contour = None
        self.highlight_color = highlight_color

    def detect_surface(self, image):
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
        if self.surface_color is not None:
            height, width = image.shape[:2]
            cv2.rectangle(image, (width-50, height-50), (width-10, height-10), self.surface_color.tolist(), -1)
            
            if self.surface_contour is not None:
                overlay = image.copy()
                cv2.drawContours(overlay, [self.surface_contour], 0, self.highlight_color, -1)
                cv2.addWeighted(overlay, 0.4, image, 0.6, 0, image)
                cv2.drawContours(image, [self.surface_contour], 0, self.highlight_color, 2)
        
        return image