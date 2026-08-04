from backend.actions.shortcut import ShortcutAction
from backend.actions.text import TextAction
from backend.actions.program import ProgramAction
from backend.actions.website import WebsiteAction




class ActionRunner:

    def __init__(self, profile_manager):
        self.profile_manager = profile_manager

        self.handlers = {

            "shortcut": ShortcutAction(),
            "text": TextAction(),
            "program": ProgramAction(),
            "website": WebsiteAction()
        }

    def run(self, action):

        print("run() received:", action)

        action_type = action.get("type")
        print("Action type:", action_type)

        handler = self.handlers.get(action_type)
        print("Handler:", handler)

        if handler is None:
            print("No handler found!")
            return False

        handler.execute(action)

        print("Executed successfully")

        return True

    def run_button(self, button_key):
    
        profile = self.profile_manager.get_active_profile()
        print("Profile:", profile)
        button = self.profile_manager.get_button(
            profile, 
            button_key
        )

        print("Button:", button)
        if not button.get("enabled", True):
            return False


        action = button.get("action", {})
        print("Action:", action)

        return self.run(action)


    def run_encoder(self, direction):

        profile = self.profile_manager.get_active_profile()

        action = self.profile_manager.get_encoder_action(
            profile, 
            direction
        )

        return self.run(action)

    def run_joystick(self, direction):
        profile = self.profile_manager.get_active_profile()
        
        action = self.profile_manager.get_joystick_action(
            profile, 
            direction
        )

        return self.run(action)