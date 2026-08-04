import keyboard
from dataclasses import dataclass


@dataclass
class Shortcut:

    keys: list[str]

    def __str__(self):

        return ShortcutRecorder.to_string(self.keys)


class ShortcutRecorder:

    MODIFIERS = [

        "ctrl",

        "shift",

        "alt",

        "windows"

    ]

    def __init__(self):

        self.recording = False

        self.current = set()

        self.recorded = []

    # ------------------------------------

    def start(self):

        self.current.clear()

        self.recorded.clear()

        self.recording = True

        keyboard.hook(self._event)

    # ------------------------------------

    def stop(self):

        keyboard.unhook_all()

        self.recording = False

        return Shortcut(

            self.sort(self.recorded)

        )

    # ------------------------------------

    def record(self):

        print("Recording shortcut...")

        self.start()

        while self.recording:
            pass

        return self.stop()

    # ------------------------------------

    def _event(self, event):

        if not self.recording:
            return  

        name = event.name.lower()

        if event.event_type == "down":

            if name not in self.current:

                self.current.add(name)

                if name not in self.recorded:

                    self.recorded.append(name)

        elif event.event_type == "up":

            if name in self.current:

                self.current.remove(name)

            if len(self.current) == 0:

                self.recording = False

            # ------------------------------------

    def sort(self, keys):

        modifiers = []

        others = []

        for key in keys:

            if key in self.MODIFIERS:

                modifiers.append(key)

            else:

                others.append(key)

        modifiers.sort(

            key=lambda x: self.MODIFIERS.index(x)

        )

        return modifiers + others

    # ------------------------------------

    @staticmethod
    def to_string(keys):

        pretty = {

            "ctrl": "Ctrl",

            "shift": "Shift",

            "alt": "Alt",

            "windows": "Win",

            "left windows": "Win",

            "right windows": "Win",

            "space": "Space",

            "enter": "Enter",

            "backspace": "Backspace",

            "esc": "Esc",

            "delete": "Delete",

            "page up": "PgUp",

            "page down": "PgDn",

            "up": "↑",

            "down": "↓",

            "left": "←",

            "right": "→"

        }

        out = []

        for key in keys:

            if key in pretty:

                out.append(pretty[key])

            elif len(key) == 1:

                out.append(key.upper())

            else:

                out.append(key.title())

        return " + ".join(out)

    # ------------------------------------

    @staticmethod
    def to_json(shortcut):

        return {

            "type": "shortcut",

            "keys": shortcut.keys

        }