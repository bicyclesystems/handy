import pyautogui

class ClickHandler:
    def __init__(self):
        self.click_state = "up"
        self.click_cooldown = 0
        self.click_cooldown_threshold = 5

    def handle_click(self, current_y, initial_y):
        if self.click_state == "up" and current_y > initial_y:
            self.click_state = "down"
            print("Click started")
        elif self.click_state == "down" and current_y < initial_y and self.click_cooldown == 0:
            self.click_state = "up"
            print("Click finished")
            pyautogui.click()
            self.click_cooldown = self.click_cooldown_threshold

        if self.click_cooldown > 0:
            self.click_cooldown -= 1

    def reset(self):
        self.click_state = "up"
        self.click_cooldown = 0