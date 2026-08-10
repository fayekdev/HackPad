import customtkinter as ctk

from ui.popups.joystick_editor import JoystickEditor

class JoystickSelector(ctk.CTkToplevel):

    DIRECTIONS = [
        ("↑ Up", "up"),
        ("↓ Down", "down"),
        ("← Left", "left"),
        ("→ Right", "right"),
        ("Press", "press")
    ]

    def __init__(
            self, 
            master, 
            profile_manager, 
            profile
    ):

        super().__init__(master)

        self.profile_manager = profile_manager
        self.profile = profile

        self.title("Joystick")

        self.geometry("260x300")

        self.resizable(False, False)

        self.transient(master)

        self.grab_set()

        ctk.CTkLabel(
            self, 
            text="Choose Direction",
            font=("Segoe UI", 18, "bold")
        ).pack(pady=(15, 10))

        for text, direction in self.DIRECTIONS:

            ctk.CTkButton(
                self, 
                text=text, 
                command=lambda d=direction: self.open_editor(d)
            ).pack(
                fill="x", 
                padx=20, 
                pady=5
            )
    def open_editor(self, direction):

        self.destroy()

        JoystickEditor(
            self.master, 
            self.profile_manager, 
            self.profile,
            direction
        )