import customtkinter as ctk

from ui.popups.action_editor import ActionEditor
from backend.constants import JOYSTICK_ACTIONS


class JoystickEditor(ctk.CTkToplevel):

    BG = "#FFFFFF"
    FG = "#000000"

    def __init__(
        self,
        master,
        backend,
        profile,
    ):
        super().__init__(master)

        self.backend = backend
        self.profile_manager = backend
        self.profile = profile

        self.title("Joystick")
        self.geometry("520x520")
        self.resizable(False, False)

        self.configure(
            fg_color=self.BG
        )

        self.transient(master)
        self.grab_set()

        self.build_ui()

    # =====================================================
    # UI
    # =====================================================

    def build_ui(self):

        self.grid_columnconfigure(
            0,
            weight=1
        )

        title = ctk.CTkLabel(
            self,
            text="Joystick",
            text_color=self.FG,
            font=("Segoe UI", 24, "bold")
        )

        title.grid(
            row=0,
            column=0,
            pady=(25, 5)
        )

        subtitle = ctk.CTkLabel(
            self,
            text="Configure each joystick action",
            text_color=self.FG,
            font=("Segoe UI", 13)
        )

        subtitle.grid(
            row=1,
            column=0,
            pady=(0, 20)
        )

        self.action_frame = ctk.CTkFrame(
            self,
            fg_color=self.BG
        )

        self.action_frame.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=30
        )

        self.action_frame.grid_columnconfigure(
            1,
            weight=1
        )

        self.create_action_row(
            0,
            "↑  Up",
            "up"
        )

        self.create_action_row(
            1,
            "↓  Down",
            "down"
        )

        self.create_action_row(
            2,
            "←  Left",
            "left"
        )

        self.create_action_row(
            3,
            "→  Right",
            "right"
        )

        self.create_action_row(
            4,
            "●  Press",
            "press"
        )

        close_button = ctk.CTkButton(
            self,
            text="Close",
            command=self.destroy,
            fg_color=self.FG,
            text_color=self.BG,
            hover_color=self.FG
        )

        close_button.grid(
            row=3,
            column=0,
            pady=25
        )

    # =====================================================
    # ACTION ROW
    # =====================================================

    def create_action_row(
        self,
        row,
        label,
        direction
    ):

        action = self.profile_manager.get_joystick_action(
            self.profile,
            direction
        )

        description = self.action_description(
            action
        )

        label_widget = ctk.CTkLabel(
            self.action_frame,
            text=label,
            text_color=self.FG,
            anchor="w",
            font=("Segoe UI", 14, "bold")
        )

        label_widget.grid(
            row=row,
            column=0,
            sticky="w",
            padx=(0, 15),
            pady=10
        )

        description_widget = ctk.CTkLabel(
            self.action_frame,
            text=description,
            text_color=self.FG,
            anchor="w"
        )

        description_widget.grid(
            row=row,
            column=1,
            sticky="ew",
            pady=10
        )

        button = ctk.CTkButton(
            self.action_frame,
            text="Configure",
            width=110,
            fg_color=self.FG,
            text_color=self.BG,
            hover_color=self.FG,
            command=lambda d=direction:
                self.open_action_editor(d)
        )

        button.grid(
            row=row,
            column=2,
            padx=(15, 0),
            pady=10
        )

    # =====================================================
    # OPEN ACTION EDITOR
    # =====================================================

    def open_action_editor(self, direction):

        ActionEditor(
            self,
            self.backend,
            title=f"Joystick — {direction.title()}",
            profile=self.profile,
            control_type="joystick",
            control=direction
        )

    # =====================================================
    # DESCRIPTION
    # =====================================================

    def action_description(self, action):

        if not action:
            return "No action"

        action_type = action.get(
            "type",
            "shortcut"
        )

        if action_type == "shortcut":

            keys = action.get(
                "keys",
                []
            )

            if not keys:
                return "No shortcut"

            return " + ".join(
                key.title()
                for key in keys
            )

        if action_type == "text":

            return action.get(
                "text",
                "No text"
            )

        if action_type == "program":

            data = action.get(
                "data",
                {}
            )

            return data.get(
                "path",
                "No program"
            )

        if action_type == "website":

            return action.get(
                "url",
                "No website"
            )

        return action_type.title()  