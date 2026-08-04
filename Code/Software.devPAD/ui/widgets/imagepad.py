from pathlib import Path

import customtkinter as ctk
from PIL import Image


class ImagePad(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.current_image = None


        self.image_path = (
            Path(__file__).resolve().parents[2]
            / "assets"
            / "HackPad.png"
        )

        self.original = Image.open(self.image_path)

        self.image_label = ctk.CTkLabel(
            self,
            text=""
        )

        self.image_label.place(
            relx=0.49,
            rely=0.45,
            anchor="center"
        )

        self.bind("<Configure>", self.resize_image)

    def resize_image(self, event=None):

        if self.winfo_width() < 50:
            return

        width = self.winfo_width() * 0.7

        ratio = self.original.height / self.original.width

        height = int(width * ratio)

        image = self.original.resize(
            (
                int(width),
                height
            )
        )

        ctk_image = ctk.CTkImage(
            light_image=image,
            dark_image=image,
            size=image.size
        )

        self.current_image = ctk_image
        self.image_label.configure(image=self.current_image)