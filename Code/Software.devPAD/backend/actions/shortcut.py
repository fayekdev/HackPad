from pynput.keyboard import Controller, Key
import time

class ShortcutAction:

    def __init__(self):

        self.keyboard = Controller()

        self.key_map = {
            "ctrl": Key.ctrl, 
            "ctrl_l": Key.ctrl,
            "ctrl_r": Key.ctrl_r,

            "shift": Key.shift,
            "shift_l": Key.shift_l,
            "shift_r": Key.shift_r,

            "alt": Key.alt,
            "alt_l": Key.alt_l,
            "alt_r": Key.alt_r,

            "cmd": Key.cmd,
            "win": Key.cmd,

            "enter": Key.enter,
            "tab": Key.tab,
            "space": Key.space,
            "backspace": Key.backspace,
            "delete": Key.delete,
            "esc": Key.esc,

            "up": Key.up,
            "down": Key.down,
            "left": Key.left,
            "right": Key.right,

            "home": Key.home,
            "end": Key.end,
            "page_up": Key.page_up,
            "page_down": Key.page_down,

            "insert": Key.insert,

            "f1": Key.f1,
            "f2": Key.f2,
            "f3": Key.f3,
            "f4": Key.f4,
            "f5": Key.f5,
            "f6": Key.f6,
            "f7": Key.f7,
            "f8": Key.f8,
            "f9": Key.f9,
            "f10": Key.f10,
            "f11": Key.f11,
            "f12": Key.f12,

            "caps_lock": Key.caps_lock,
            "num_lock": Key.num_lock,
            "scroll_lock": Key.scroll_lock,

            "print_screen": Key.print_screen,
            "pause": Key.pause,
            "menu": Key.menu,

            "volume up": Key.media_volume_up,
            "volume down": Key.media_volume_down,
            "mute": Key.media_volume_mute,

            "play": Key.media_play_pause,
            "next": Key.media_next,
            "previous": Key.media_previous
        }

    def execute(self, action):

        keys = action.get("keys", [])

        if not keys:
            return
        
        pressed = []

        try:
            for key in keys:

                lookup = key.lower()

                if lookup in self.key_map:
                    mapped = self.key_map[lookup]
                else:
                    mapped = lookup

                self.keyboard.press(mapped)
                pressed.append(mapped)
            time.sleep(0.05)

        finally:
            for key in reversed(pressed):
                self.keyboard.release(key)