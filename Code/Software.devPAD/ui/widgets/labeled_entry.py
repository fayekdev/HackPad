import customtkinter as ctk

class LabeledEntry(ctk.CTkFrame):

    def __init__(self, master, label):

        super().__init__(
            master, 
            fg_color="transparent"
        )

        self.title = ctk.CTkLabel(
            self, 
            text=label, 
            text_color="black"
        )

        self.title.pack(
            anchor="w"
        )

        self.entry= ctk.CTkEntry(
            self,
            height=38
        )

        self.entry.pack(
            fill="x",
            pady=(4, 0)
        )

    def get(self):
            return self.entry.get

    def set(self, value):
         self.entry.delete(0, "end")
         self.entry.insert(0, value)







