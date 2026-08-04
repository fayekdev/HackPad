APP_NAME = ".devPAD"
APP_VERSION = "0.1.0"



DEFAULT_PROFILE = "Default"


BUTTON_COUNT = 14

BUTTON_KEYS = [
    f"key_{i}" for i in range(1, BUTTON_COUNT + 1)
]

ENCODER_ACTIONS = (
    "clockwise",
    "counter_clockwise",
    "press"
)

JOYSTICK_ACTIONS = (
    "up",
    "down",
    "left",
    "right",
    "press"
)

DISPLAY_ID = "display"

ACTION_SHORTCUT = "shortcut"
ACTION_TEXT = "text"
ACTION_PROGRAM = "program"
ACTION_WEBSITE = "website"

ACTION_TYPES = [
    ACTION_SHORTCUT,
    ACTION_TEXT,
    ACTION_PROGRAM,
    ACTION_WEBSITE
]

DEFAULT_ACTION = {
    "type": ACTION_SHORTCUT, 
    "keys": []
}