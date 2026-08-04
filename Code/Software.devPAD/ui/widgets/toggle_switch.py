import customtkinter as ctk

class ToggleSwitch(ctk.CTkSwitch):

    def __init__(self, master):

        super().__init__(
            master,
            text="Enabled"
        )