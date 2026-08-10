import customtkinter as ctk

from backend.constants import ENCODER_ACTIONS, ACTION_TYPES
from backend.shortcut_recorder import ShortcutRecorder


class EncoderEditor(ctk.CTkToplevel):

    def __init__(
        self,
        master,
        profile_manager,
        profile
    ):
        super().__init__(master)

        self.profile_manager = profile_manager
        self.profile = profile

        self.title("Encoder Settings")
        self.geometry("600x500")
        self.resizable(False, False)

        self.transient(master)
        self.grab_set()

        self.recorder = ShortcutRecorder()

        self.actions = {}

        self.build_ui()
        self.load_actions()

    # --------------------------------------------------

    def build_ui(self):

        self.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            self,
            text="Encoder Settings",
            font=("Segoe UI", 22, "bold")
        )

        title.grid(
            row=0,
            column=0,
            pady=(20, 15)
        )

        self.content = ctk.CTkFrame(self)

        self.content.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=25,
            pady=10
        )

        self.content.grid_columnconfigure(1, weight=1)

        row = 0

        for direction in ENCODER_ACTIONS:

            label = ctk.CTkLabel(
                self.content,
                text=direction.replace("_", " ").title()
            )

            label.grid(
                row=row,
                column=0,
                padx=10,
                pady=12,
                sticky="w"
            )

            entry = ctk.CTkEntry(
                self.content
            )

            entry.grid(
                row=row,
                column=1,
                padx=10,
                pady=12,
                sticky="ew"
            )

            button = ctk.CTkButton(
                self.content,
                text="Edit",
                width=80,
                command=lambda d=direction: self.edit_action(d)
            )

            button.grid(
                row=row,
                column=2,
                padx=10,
                pady=12
            )

            self.actions[direction] = entry

            row += 1

        self.button_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.button_frame.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=25,
            pady=20
        )

        ctk.CTkButton(
            self.button_frame,
            text="Cancel",
            command=self.destroy
        ).pack(
            side="right",
            padx=5
        )

        ctk.CTkButton(
            self.button_frame,
            text="Save",
            command=self.save
        ).pack(
            side="right",
            padx=5
        )

    # --------------------------------------------------

    def load_actions(self):

        for direction in ENCODER_ACTIONS:

            action = self.profile_manager.get_encoder_action(
                self.profile,
                direction
            )

            text = self.action_to_string(action)

            self.actions[direction].insert(
                0,
                text
            )

    # --------------------------------------------------

    def action_to_string(self, action):

        if not action:
            return ""

        action_type = action.get("type")

        if action_type == "shortcut":
            return ShortcutRecorder.to_string(
                action.get("keys", [])
            )

        if action_type == "text":
            return action.get("text", "")

        if action_type == "program":
            return action.get("path", "")

        if action_type == "website":
            return action.get("url", "")

        return ""

    # --------------------------------------------------

    def edit_action(self, direction):

        from ui.popups.action_editor import ActionEditor

        action = self.profile_manager.get_encoder_action(
            self.profile,
            direction
        )

        editor = ActionEditor(
            self,
            self.profile_manager,
            self.profile,
            "encoder",
            direction,
            action
        )

        self.wait_window(editor)

        self.actions[direction].delete(0, "end")

        action = self.profile_manager.get_encoder_action(
            self.profile,
            direction
        )

        self.actions[direction].insert(
            0,
            self.action_to_string(action)
        )

    # --------------------------------------------------

    def save(self):

        self.destroy()