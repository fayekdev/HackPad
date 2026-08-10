import customtkinter as ctk

from backend.tracker import TrackerService
from ui.dashboard import Dashboard
from backend.profile_manager import ProfileManager

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

        self.tracker = TrackerService()
        self.profile_manager = ProfileManager()
        self.tracker.start()

        self.dashboard = Dashboard(
            self,
            self.profile_manager

        ).pack(
            fill="both",
            expand=True
        )

        self.protocol(
            "WM_DELETE_WINDOW",
            self.close
        )

    def close(self):

        self.tracker.stop()

        self.destroy()