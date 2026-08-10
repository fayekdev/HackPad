import customtkinter as ctk


class ProfileBar(ctk.CTkFrame):
    

    ACTIVE_COLOR = "#222222"
    ACTIVE_TEXT = "#FFFFFF"

    INACTIVE_COLOR = "#706B6B"
    INACTIVE_TEXT = "#222222"

    BORDER = "#222222"

    def __init__(self, master, profile_manager, callback=None,):
        super().__init__(
            master,
            fg_color="transparent",
            height=48
        )
        
        self.callback = callback
        self.profile_manager = profile_manager
        self.buttons = {}

        self.pack_propagate(False)

        self.container = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.container.pack(
            side="left",
            fill="x",
            expand=True
        )

        self.refresh()

    # --------------------------------------------------

    def refresh(self):

        
        profiles = self.profile_manager.get_profile_names()

        if set(profiles) != set(self.buttons.keys()):

            for widget in self.container.winfo_children():
                widget.destroy()

            self.buttons.clear()

            for profile in profiles:

                btn = ctk.CTkButton(

                    self.container,

                    text=profile,

                    width=110,

                    height=34,

                    corner_radius=10,

                    border_width=2,

                    border_color=self.BORDER,

                    fg_color=self.INACTIVE_COLOR,

                    text_color=self.INACTIVE_TEXT,

                    hover_color="#131111",

                    command=lambda p=profile: self.select(p)

                )

                btn.pack(
                    side="left",
                    padx=5
                )

                self.buttons[profile] = btn

        self.highlight(self.profile_manager.get_active_profile())

        self.after(
            250,
            self.refresh
        )

    # --------------------------------------------------

    def highlight(self, current):

        for profile, button in self.buttons.items():

            if profile == current:

                button.configure(

                    fg_color=self.ACTIVE_COLOR,

                    text_color=self.ACTIVE_TEXT

                )

            else:

                button.configure(

                    fg_color=self.INACTIVE_COLOR,

                    text_color=self.INACTIVE_TEXT

                )

    # --------------------------------------------------

    def select(self, profile):

        self.profile_manager.set_active_profile(profile)

        self.highlight(profile)

        if self.callback is not None:

            self.callback(profile)