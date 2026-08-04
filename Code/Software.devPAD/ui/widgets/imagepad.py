from pathlib import Path

import tkinter as tk
import customtkinter as ctk

from PIL import Image, ImageTk

from backend.layout import HITBOXES


class ImagePad(ctk.CTkFrame):

    def __init__(self, master, callback=None):

        super().__init__(master, fg_color="transparent")

        self.callback = callback

        self.image_path = (
            Path(__file__).resolve().parents[2]
            / "assets"
            / "image-removebg-preview.png"
        )

        self.original = Image.open(self.image_path)

        self.canvas = tk.Canvas(
            self,
            bg="#ECECEC",
            highlightthickness=0
        )

        self.canvas.pack(fill="both", expand=True)

        self.tk_image = None
        self.image_width = 0
        self.image_height = 0
        self.image_x = 0
        self.image_y = 0

        self.debug = False

        self.bind("<Configure>", self.redraw)
        self.canvas.bind("<Button-1>", self.click)

    # ------------------------------------------------

    def redraw(self, event=None):

        w = self.winfo_width()
        h = self.winfo_height()

        if w < 20 or h < 20:
            return

        scale = min(
            w / self.original.width,
            h / self.original.height
        ) * 0.90

        self.image_width = int(self.original.width * scale)
        self.image_height = int(self.original.height * scale)

        resized = self.original.resize(
            (
                self.image_width,
                self.image_height
            )
        )

        self.tk_image = ImageTk.PhotoImage(resized)

        self.canvas.delete("all")

        self.image_x = (w - self.image_width) // 2
        self.image_y = (h - self.image_height) // 2

        self.canvas.create_image(
            self.image_x,
            self.image_y,
            image=self.tk_image,
            anchor="nw"
        )

        if self.debug:
            self.draw_hitboxes()

    # ------------------------------------------------

    def draw_hitboxes(self):

        for name, box in HITBOXES.items():

            cx, cy, bw, bh = box

            x1 = self.image_x + (cx - bw / 2) * self.image_width
            y1 = self.image_y + (cy - bh / 2) * self.image_height

            x2 = self.image_x + (cx + bw / 2) * self.image_width
            y2 = self.image_y + (cy + bh / 2) * self.image_height

            
    # ------------------------------------------------

    def click(self, event):

        control = self.hit_test(
            event.x,
            event.y
        )

        if control:

            print(control)

            if self.callback:
                self.callback(control)

    # ------------------------------------------------

    def hit_test(self, x, y):

        for name, box in HITBOXES.items():

            cx, cy, bw, bh = box

            x1 = self.image_x + (cx - bw / 2) * self.image_width
            y1 = self.image_y + (cy - bh / 2) * self.image_height

            x2 = self.image_x + (cx + bw / 2) * self.image_width
            y2 = self.image_y + (cy + bh / 2) * self.image_height

            if x1 <= x <= x2 and y1 <= y <= y2:
                return name

        return None

    # ------------------------------------------------

    def enable_debug(self):

        self.debug = True
        self.redraw()

    def disable_debug(self):

        self.debug = False
        self.redraw()
