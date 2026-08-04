import customtkinter as ctk


class RecordButton(ctk.CTkButton):

    def __init__(self, master, command):
        super().__init__(
            master, 
            text="•Record", 
            command=command,
            fg_color="white",
            text_color="black", 
            hover_color="#DDDDDD",
            border_width=2,
            border_color="black",
            corner_radius=12,
            height=42

        )