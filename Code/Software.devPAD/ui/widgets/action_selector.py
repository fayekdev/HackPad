import customtkinter as ctk


class ActionSelector(ctk.CTkOptionMenu):

    def __init__(self, master, command=None):

        super().__init__(
            master, 
            values=[

                "Shortcut", 

                "Program",

                "Text",

                "Macro",

                "Mouse",

                "Media"
            ],

            command=command, 
            height=38

        )