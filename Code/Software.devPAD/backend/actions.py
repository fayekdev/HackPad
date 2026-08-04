from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

@dataclass 
class Action:

    type: str = "shortcut"
    def to_dict(self) -> dict[str, Any]:
        raise NotImplementedError

@dataclass 
class ShortcutAction(Action):

    keys: list[str] = field(default_factory=list)

    def __init__(self, keys=None):
        self.type = "shortcut"
        self.keys = keys or []

    def to_dict(self):

        return {
            "type": self.type,
            "keys": self.keys
        }

@dataclass
class ProgramAction(Action):
    path: str =""
    arguments: str = ""

    def __init__(self, path="", arguments=""):

        self.type = "program"
        self.path = "path"

    def to_dict(self):

        return{
            "typr": self.type,
            "path": self.path,
            "arguments": self.arguments
        }

@dataclass
class TextAction(Action):

    text: str= ""

    def __init__(self, text=""):
        self.type = "text"
        self.text = text
    def to_dict(self):

        return {
            "type": self.type,
            "text": self.text
        }
def action_from_dict(data: dict):
    t = data.get("type", "shortcut")

    if t == "shortcut":
        return ShortcutAction(data.get("keys", []))

    if t == "program":
        return ProgramAction(
            data.get("path", ""),
            data.get("arguments", "")
    
        )
    if t == "text":
        return TextAction(
            data.get("text", "")
        )

    return ShortcutAction()
    