import customtkinter as ctk


class ShortcutDisplay(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(
            master,
            fg_color="#F4F4F4",
            corner_radius=12,
            border_width=2,
            border_color="#000000"
        )

        self.label = ctk.CTkLabel(
            self,
            text="No Shortcut",
            font=("Arial", 18, "bold"),
            text_color="black"
        )

        self.label.pack(
            padx=15,
            pady=12
        )

    def set_shortcut(self, text):

        self.label.configure(text=text)