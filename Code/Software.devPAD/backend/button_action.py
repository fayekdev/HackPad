from dataclasses import dataclass, field
from typing import List


@dataclass
class ButtonAction:
    key: str

    name: str = ""

    action: str = "shortcut"

    shortcut: List[str] = field(default_factory=list)

    program: str = ""

    arguments: str = ""

    text: str = ""

    enabled: bool = True

    def to_dict(self):

        return {
            "key": self.key,
            "name": self.name,
            "action": self.action,
            "shortcut": self.shortcut,
            "program": self.program,
            "arguments": self.arguments,
            "text": self.text,
            "enabled": self.enabled,
        }

    @classmethod
    def from_dict(cls, data):

        return cls(
            key=data.get("key", ""),
            name=data.get("name", ""),
            action=data.get("action", "shortcut"),
            shortcut=data.get("shortcut", []),
            program=data.get("program", ""),
            arguments=data.get("arguments", ""),
            text=data.get("text", ""),
            enabled=data.get("enabled", True),
        )