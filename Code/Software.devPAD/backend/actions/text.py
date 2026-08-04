from pynput.keyboard import Controller
import time

class TextAction:

    def __init__(self):
        self.keyboard = Controller()

    def execute(self, action):

        if "data" in action:
            text = action["data"].get("text", "")
        else: 
            text = action.get("text", "")

        if not text:
            return
        time.sleep(0.05)

        self.keyboard.type(text)