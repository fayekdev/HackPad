import customtkinter as ctk
from tkinter import filedialog
import threading

from backend.constants import ACTION_TYPES
from backend.shortcut_recorder import ShortcutRecorder

class ActionEditor(ctk.CTkToplevel):


    def __init__(
        self,
        master,
        profile_manager,
        profile,
        control_type,
        control,
        title
    ):

        super().__init__(master)

        self.profile_manager = profile_manager
        self.profile = profile
        self.control_type = control_type
        self.control = control

        self.title(title)

        self.geometry("650x520")

        self.resizable(False, False)

        self.transient(master)

        self.grab_set()

        self.shortcut_recorder = ShortcutRecorder()

        self._current_action = {
            "type": "shortcut",
            "keys": []
        }

        self.build_ui()
        self.load_action()
        
        
    def build_ui(self):

        self.grid_columnconfigure(0, weight=1)

        self.titleLabel = ctk.CTkLabel(
            self, 
            text=self.title(), 
            font=("Sego UI", 22, "bold")
        )

        self.titleLabel.grid(
            row=0,
            column=0,
            pady=(20, 10)
        )

        self.typeLabel = ctk.CTkLabel(
            self, 
            text="Action Type"
        )

        self.typeLabel.grid(
            row=1, 
            column=0,
            sticky="w",
            padx=25
        )

        self.typeMenu = ctk.CTkOptionMenu(
            self, 
            values=ACTION_TYPES, 
            command=self.update_fields
        )

        self.typeMenu.grid(
            row=2,
            column=0, 
            sticky="ew",
            padx=25, 
            pady=(0,15)
        )

        self.contentFrame = ctk.CTkFrame(self)

        self.contentFrame.grid(
            row=3,
            column=0, 
            sticky="nsew", 
            padx=25, 
            pady=10
        )

        self.contentFrame.grid_columnconfigure(
            0, 
            weight=1
        )

        self.buttonFrame = ctk.CTkFrame(
            self, 
            fg_color="transparent"
        )

        self.buttonFrame.grid(
            row=4, 
            column=0, 
            sticky="ew", 
            padx=25, 
            pady=20
        )

        self.cancelButton = ctk.CTkButton(
            self.buttonFrame, 
            text="Cancel",
            command=self.destroy
        )

        self.cancelButton.pack(
            side="right", 
            padx=5
        )

        self.saveButton = ctk.CTkButton(
            self.buttonFrame, 
            text="Save", 
            command=self.save_action
        )

        self.saveButton.pack(
            side="right", 
            padx=5
        )

        self.build_shortcut_frame()
        self.build_text_frame()
        self.build_program_frame()
        self.build_website_frame()

        self.update_fields("shortcut")

    def build_shortcut_frame(self):
        self.shortcutFrame = ctk.CTkFrame(self.contentFrame)

        self.shortcutFrame.grid_columnconfigure(0, weight=1)


        self.shortcutEntry = ctk.CTkEntry(
            self.shortcutFrame, 
            state="readonly"
        )


        self.shortcutEntry.grid(
            row=0,
            column=0, 
            sticky="ew",
            padx=10, 
            pady=15
        )

        self.recordButton = ctk.CTkButton(
            self.shortcutFrame, 
            text="Record Shortcut", 
            command=self.record_shortcut
        )

        self.recordButton.grid(
            row=1, 
            column=0, 
            padx=10, 
            pady=(0, 15)
        )


    def build_text_frame(self):

        self.textFrame = ctk.CTkFrame(self.contentFrame)
        self.textFrame.grid_columnconfigure(0, weight=1)
        self.textBox = ctk.CTkTextbox(
            self.textFrame, 
            height=220
        )

        self.textBox.grid(
            row=0, 
            column=0, 
            sticky="nsew", 
            padx=10, 
            pady=10
        )

        
    def build_program_frame(self):
        self.programFrame = ctk.CTkFrame(self.contentFrame)
        self.programFrame.grid_columnconfigure(0, weight=1)
        self.programEntry = ctk.CTkEntry(
            self.programFrame
        )

        self.programEntry.grid(
            row=0,
            column=0, 
            sticky="ew", 
            padx=10, 
            pady=(15, 10)
        )


        self.browseButton = ctk.CTkButton(
            self.programFrame, 
            text="Browse...", 
            command=self.browse_program
        )

        self.browseButton.grid(
            row=0, 
            column=1, 
            padx=(5, 10), 
            pady=(15, 10)
        )

        self.argsLabel = ctk.CTkLabel(
            self.programFrame, 
            text="Arguments"
        )

        self.argsLabel.grid(
            row=1, 

            column=0, 
            sticky="w", 
            padx=10
        )

        self.argsEntry = ctk.CTkEntry(
            self.programFrame
        )

        self.argsEntry.grid(
            row=2, 
            column=0, 
            columnspan=2, 
            sticky="ew", 
            padx=10,
            pady=(5, 15)
        )

    def build_website_frame(self):

        self.websiteFrame = ctk.CTkFrame(self.contentFrame)

        self.contentFrame.grid_columnconfigure(0, weight=1)

        self.websiteEntry = ctk.CTkEntry(
            self.websiteFrame, 
            placeholder_text="https://example.com"
        )

        self.websiteEntry.grid(
            row=0, 
            column=0, 
            sticky="ew", 
            padx=10, 
            pady=15
        )

    def update_fields(self, action_type):

        for frame in (
            self.shortcutFrame, 
            self.textFrame, 
            self.programFrame, 
            self.websiteFrame
        ):
            frame.grid_forget()

        if action_type == "shortcut":

            self.shortcutFrame.grid(
                row=0, 
                column=0, 
                sticky="nsew"
            )
        elif action_type == "text":

            self.textFrame.grid(
                row=0, 
                column=0, 
                sticky="nsew"
            )

        elif action_type == "program":
            self.programFrame.grid(
                row=0, 
                column=0, 
                sticky="nsew"
            )

        elif action_type == "website":

            self.websiteFrame.grid(
                row=0, 
                column=0, 
                sticky="nsew"
            )


    def record_shortcut(self):

        self.shortcutEntry.configure(state="normal")
        self.shortcutEntry.delete(0, "end")
        self.shortcutEntry.insert(0, "Recording...")
        self.shortcutEntry.configure(state="readonly")

        thread = threading.Thread(

            target=self._record_thread, 
            daemon=True

        )

        thread.start()

    def _record_thread(self):

        shortcut = self.shortcut_recorder.record()

        self.after(
            0,
            lambda: self._finish_record(shortcut)
        ) 

    def get_action(self):

        if self.control_type == "button":
            button = self.profile_manager.get_button(
                self.profile, 
                self.control
            )

        elif self.control_type == "encoder":
            return self.profile_manager.get_encoder_action(
                self.profile,
                self.control
            )
        elif self.control_type == "joystick":

            return self.profile_manager.get_joystick_action(
                self.profile, 
                self.control
            )
        return {
            "type": "shortcut",
            "keys": []
        }

    def _finish_record(self, shortcut):

        self._current_action = {
            "type": "shortcut",
            "keys": shortcut.keys
        }

        self.shortcutEntry.configure(state="normal")
        self.shortcutEntry.delete(0, "end")
        self.shortcutEntry.insert(
            0, 
            str(shortcut)
        )

        self.shortcutEntry.configure(state="readonly")

    def browse_program(self):
        filename = filedialog.askopenfilename(
            title="Select Program"
        )

        if not filename:
            return
        self.programEntry.delete(
            0, 
            "end"
        )

        self.programEntry.insert(
            0, 
            filename
        )

    def load_action(self):

        action = self.get_action()

        self._current_action = action 

        action_type = action.get(
            "type",
            "shortcut",
        )

        self.typeMenu.set(action_type)

        self.update_fields(action_type)

        if action_type == "shortcut":
            keys = action.get("keys", [])
            self.shortcutEntry.configure(state="normal")
            self.shortcutEntry.delete(0, "end")
            self.shortcutEntry.insert(
                0,
                ShortcutRecorder.to_string(keys)
            )

            self.shortcutEntry.configure(state="readonly")

        elif action_type == "text":

            self.textBox.delete("1.0", "end")

            self.textBox.insert(
                "1.0", 
                action.get("text", "")
            )

        elif action_type == "program":

            data = action.get("data", {})

            self.programEntry.insert(
                0, 
                data.get("path", "")
            )

            self.argsEntry.delete(0, "end")


            self.argsEntry.insert(
                0, 
                data.get("args", "")
            )

        elif action_type == "website":

            self.websiteEntry.delete(0, "end")

            self.websiteEntry.insert(
                0, 
                action.get("url", "")
            )

    def build_action(self):

        action_type = self.typeMenu.get()

        if action_type == "shortcut":
            return self._current_action

        elif action_type == "text":

            return{
                "type": "text", 
                "text": self.textBox.get(
                    "1.0", 
                    "end-1c"
                )
            }

        elif action_type == "program":

            return {
                "type": "program", 
                "data": {
                    "path": self.programEntry.get(),
                    "args": self.argsEntry.get()
                }
            }

        elif action_type == "website":

            return {
                "type": "website", 
                "url": self.websiteEntry.get()
            }

        return {
            "type": "shortcut", 
            "keys": []
        }

    
    def save_action(self):


        action = self.build_action()

        if self.control_type == "button":

            button = self.profile_manager.get_button(
                self.profile,
                self.control
            )

            button["action"] = action

            self.profile_manager.update_button(
                self.profile, 
                self.control, 
                button
            )

        elif self.control_type == "encoder":

            self.profile_manager.update_encoder_action(
                self.profile, 
                self.control, 
                action
            )
        elif self.control_type == "joystick":

            self.profile_manager.update_joystick_action(
                self.profile, 
                self.control, 
                action
            )

        self.destroy()