import pyautogui

class SlideController:

    @staticmethod
    def next_slide():
        print("Próximo slide")
        pyautogui.press('right')  # Avançar slide

    @staticmethod
    def prev_slide():
        print("Slide anterior")
        pyautogui.press('left')   # Retroceder slide
