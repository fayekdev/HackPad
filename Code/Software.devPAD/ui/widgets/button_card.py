import customtkinter as ctk

class ButtonCard(ctk.CTkFrame):

    def __init__(self, master, title, subtitle=""):

        super().__init__(
            master, 
            corner_radius=14,
            border_width=2,
            border_color="black",
            fg_color="White"
        )

        ctk.CTkLabel(
            self,
            text=subtitle,
            text_color="gray30",

        ).pack(
            anchor="w",
            padx=15,
            pady=(0, 10)
        )