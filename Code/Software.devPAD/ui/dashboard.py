import customtkinter as ctk

from ui.widgets.imagepad import ImagePad
from ui.widgets.profilebar import ProfileBar


from ui.popups.button_editor import ButtonEditor
from ui.popups.encoder_editor import EncoderEditor
from ui.popups.joystick_editor import JoystickEditor

class Dashboard(ctk.CTkFrame):

    def control_clicked(self, control):
        print(f"Clicked: {control}")

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

        self.pad = ImagePad(
            self,
            callback=self.control_clicked
        )

        self.pad.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )