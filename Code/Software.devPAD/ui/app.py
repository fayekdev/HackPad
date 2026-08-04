import customtkinter as ctk

from backend import TrackerService
from ui.dashboard import Dashboard


ctk.set_appearance_mode("light")

ctk.set_default_color_theme("blue")


class DevPadApp(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.title(".devPAD")

        self.geometry("900x600")
        self.minsize(600, 300)
        self.resizable(True, True)

        self.configure(
            fg_color="#ECECEC"
        )

        self.backend = TrackerService()

        self.backend.start()

        Dashboard(
            self,
            self.backend
        ).pack(
            fill="both",
            expand=True
        )

        self.protocol(
            "WM_DELETE_WINDOW",
            self.close
        )

    def close(self):

        self.backend.stop()

        self.destroy()