from ui.popups.action_editor import ActionEditor


class EncoderEditor(ActionEditor):

    def __init__(
        self, 
        master, 
        profile_manager, 
        profile, 
        direction

    ):
        super().__init__(
            master=master, 
            profile_manager=profile_manager, 
            profile=profile, 
            control_type="encoder", 
            control=direction
        )