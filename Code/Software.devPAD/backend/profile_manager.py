from pathlib import Path
import json



from backend.constants import (
    DEFAULT_PROFILE,
    DEFAULT_ACTION,
    BUTTON_KEYS,
    ENCODER_ACTIONS,
    JOYSTICK_ACTIONS
)
class ProfileManager:

    print("Loaded PM...")

    def __init__(self):

        self.file = (
            Path(__file__).resolve().parents[1]
            / "profiles.json"
        )

        if not self.file.exists():
            self._create_default()


        self.load()

    # =====================================================
    # File Management
    # =====================================================

    def _create_default(self):

        self.data = {
            "active_profile": DEFAULT_PROFILE,
            "profiles": {
                DEFAULT_PROFILE: {
                    "buttons": {},
                    "encoder": {},
                    "joystick": {}
                }
            }
        }

        self.save()

            
    
    def load(self):

        with open(
            self.file,
            "r", 
            encoding="utf8"
        ) as f:

            self.data = json.load(f)

        if "active_profile" not in self.data:
            self.data["active_profile"] = DEFAULT_PROFILE

    def save(self):

        with open(self.file, "w", encoding="utf8") as f:
            json.dump(
                self.data,
                f,
                indent=4
            )

    # =====================================================
    # Active Profile
    # =====================================================

    def get_active_profile(self):

        return self.data["active_profile"]

    def set_active_profile(self, profile):

        if profile not in self.data["profiles"]:
            return False

        self.data["active_profile"] = profile
        self.save()
        return True

        

    # =====================================================
    # Profile Functions
    # =====================================================

    def get_profile_names(self):

        return list(self.data["profiles"].keys())

    def has_profile(self, name):

        return name in self.data["profiles"]

    def create_profile(self, name):

        if self.has_profile(name):
            return False

        self.data["profiles"][name] = {
            "buttons": {},
            "encoder": {},
            "joystick": {}

        }

        self.save()
        
    def delete_profile(self, name):

        if name == DEFAULT_PROFILE:
            return False

        if not self.has_profile(name):
            return False

        del self.data["profiles"][name]

        if self.get_active_profile() == name:

            self.set_active_profile(
                DEFAULT_PROFILE
            )

        self.save()

    def rename_profile(
        self, 
        old_name, 
        new_name
    ):

        if not self.has_profile(old_name):
            return False

        if self.has_profile(new_name):
            return False

        self.data["profiles"][new_name] = \
            self.data["profiles"].pop(old_name)
        

        if self.get_active_profile() == old_name:
            self.set_active_profile(
                new_name
            )

        self.save()
        return True

    def _profile(self, profile):
         return self.data["profiles"][profile]

    def _default_action(self):
        return dict(DEFAULT_ACTION)
    # =====================================================
    # Button Functions
    # =====================================================

    def get_button(self, profile, key):

        buttons = self._profile(profile)["buttons"]

        if key not in buttons:
        
            buttons[key] = {
            
                "name": "",
                "enabled": True,
                "action": self._default_action()  
            }
        
            self.save()

        return buttons[key]

    
    def update_button(
        self,
        profile, 
        key, 
        button_data):

        self._profile(profile)["buttons"][key] = button_data

        self.save()

    # =====================================================
    # Encoder Functions
    # =====================================================

    def get_encoder_action(
        self, 
        profile, 
        direction
    ):

        encoder = self._profile(profile)["encoder"]

        if direction not in encoder:
            encoder[direction] = self._default_action()
            self.save()

        return encoder[direction]

    def update_encoder_action(
        self,
        profile,
        direction,
        action
    ):

        self._profile(profile)["encoder"][direction] = action

        self.save()

    # =====================================================
    # Joystick Functions
    # =====================================================

    def get_joystick_action(
        self, 
        profile, 
        direction
    ):

        joystick = self._profile(profile)["joystick"]

        if direction not in joystick:

            joystick[direction] = self._default_action()
            self.save()
        return joystick[direction]

    def update_joystick_action(
        self,
        profile,
        direction,
        action
    ):

        self._profile(profile)["joystick"][direction] = action

        self.save()

    # =====================================================
    # Utility Functions
    # =====================================================

    def get_all_buttons(self, profile):
        buttons = {}

        for key in BUTTON_KEYS:

            buttons[key] = self.get_button(
                profile,
                key
            )
        return buttons
    def get_encoder(self, profile):

        encoder ={}

        for direction in ENCODER_ACTIONS:

            encoder[direction] = self.get_encoder_action(
                profile,
                direction
            )
        return encoder

    def get_joystick(self, profile):

            joystick ={}
    
            for direction in JOYSTICK_ACTIONS:
    
                joystick[direction] = self.get_joystick_action(
                    profile,
                    direction
                )
            return joystick
    
        