import cv2
import numpy as np

class CoordinateSystem:
    def __init__(self):
        self.show_palm_axes = False
        self.show_finger_axes = [False] * 5  # For thumb, index, middle, ring, pinky
        self.button_pos = (10, 50)
        self.button_size = (225, 50)
        self.finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']

    def draw_coordinate_system(self, image, center, direction, scale=100):
        y_vector = direction
        length = np.sqrt(y_vector[0]**2 + y_vector[1]**2)
        y_vector = (int(y_vector[0] / length * scale), int(y_vector[1] / length * scale))

        x_vector = (-y_vector[1], y_vector[0])

        z_vector = (0, -scale)

        cv2.arrowedLine(image, center, (center[0] + x_vector[0], center[1] + x_vector[1]), (0, 0, 255), 2)
        cv2.arrowedLine(image, center, (center[0] + y_vector[0], center[1] + y_vector[1]), (0, 255, 0), 2)
        cv2.arrowedLine(image, center, (center[0] + z_vector[0], center[1] + z_vector[1]), (255, 0, 0), 2)

        cv2.putText(image, "X", (center[0] + x_vector[0] + 10, center[1] + x_vector[1] + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        cv2.putText(image, "Y", (center[0] + y_vector[0] + 10, center[1] + y_vector[1] + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        cv2.putText(image, "Z", (center[0] + z_vector[0], center[1] + z_vector[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

        return image

    def draw_hand_axes(self, image, hand_info):
        if self.show_palm_axes:
            image = self.draw_coordinate_system(image, hand_info['palm_center'], hand_info['hand_direction'])

        for i, (tip, direction) in enumerate(zip(hand_info['finger_tips'], hand_info['finger_directions'])):
            if self.show_finger_axes[i]:
                image = self.draw_coordinate_system(image, tip, direction, scale=50)

        return image

    def draw_buttons(self, image):
        button_text = "Hide Palm Axes" if self.show_palm_axes else "Show Palm Axes"
        self.draw_button(image, button_text, self.button_pos, self.button_size)

        for i, finger in enumerate(self.finger_names):
            finger_button_pos = (self.button_pos[0], self.button_pos[1] + (i + 1) * (self.button_size[1] + 5))
            button_text = f"Hide {finger} Axes" if self.show_finger_axes[i] else f"Show {finger} Axes"
            self.draw_button(image, button_text, finger_button_pos, self.button_size)

    def draw_button(self, image, text, position, size):
        x, y = position
        w, h = size
        cv2.rectangle(image, (x, y), (x + w, y + h), (200, 200, 200), -1)
        cv2.putText(image, text, (x + 5, y + h - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 1)

    def handle_click(self, x, y):
        if self.is_mouse_over_button((x, y), self.button_pos, self.button_size):
            self.show_palm_axes = not self.show_palm_axes
        for i in range(5):
            finger_button_pos = (self.button_pos[0], self.button_pos[1] + (i + 1) * (self.button_size[1] + 5))
            if self.is_mouse_over_button((x, y), finger_button_pos, self.button_size):
                self.show_finger_axes[i] = not self.show_finger_axes[i]

    def is_mouse_over_button(self, mouse_pos, button_pos, button_size):
        return (button_pos[0] < mouse_pos[0] < button_pos[0] + button_size[0] and
                button_pos[1] < mouse_pos[1] < button_pos[1] + button_size[1])