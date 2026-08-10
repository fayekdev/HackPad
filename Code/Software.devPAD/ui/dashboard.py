import customtkinter as ctk

from ui.widgets.imagepad import ImagePad
from ui.widgets.profilebar import ProfileBar


from ui.popups.button_editor import ButtonEditor
from ui.popups.encoder_editor import EncoderEditor
from ui.popups.joystick_editor import JoystickEditor
from ui.popups.tasks_popup import TasksPopup
class Dashboard(ctk.CTkFrame):

    def control_clicked(self, control):

        profile = self.profile_manager.get_active_profile()

        print(f"Control Clicked: {control}")
        print(f"Active Profile: {profile}")

        if control.startswith("key_"):

            ButtonEditor(
                self, 
                self.profile_manager, 
                profile, 
                control
            )

        elif control == "encoder":

            EncoderEditor(
                self, 
                self.profile_manager, 
                profile, 
                
            )

        elif control == "joystick":

            JoystickEditor(
                self, 
                self.profile_manager, 
                profile, 
                
            )

        elif control == "display":

            TasksPopup(
                self, 
            )
        else :
            print(f"Unknown Control: {control}")

    def __init__(self, master, profile_manager):

        super().__init__(
            master,
            fg_color="#FFFFFF"
        )

        self.profile_manager = profile_manager

        self.profilebar = ProfileBar(
            self,
            self.profile_manager
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