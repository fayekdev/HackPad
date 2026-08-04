import customtkinter as ctk

from ui.widgets.imagepad import ImagePad
from ui.widgets.profilebar import ProfileBar


class Dashboard(ctk.CTkFrame):

    def __init__(self, master, backend):

        super().__init__(
            master,
            fg_color="#ECECEC"
        )

        self.backend = backend

        self.profilebar = ProfileBar(
            self,
            backend
        )

        self.profilebar.pack(
            fill="x",
            padx=20,
            pady=(15, 5)
        )

        self.pad = ImagePad(self)

        self.pad.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )