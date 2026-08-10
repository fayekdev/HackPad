from ui.popups.action_editor import ActionEditor


class ButtonEditor(ActionEditor):

    def __init__(
        self, 
        master, 
        profile_manager, 
        profile, 
        button

    ):
        super().__init__(
            master=master, 
            profile_manager=profile_manager, 
            profile=profile, 
            control_type="button", 
            control=button,
            title=f"Edit {button}"
        )

        