import customtkinter as ctk

class SectionTitle(ctk.CTkLabel):
    
    def __init__(self, master, text):
        super().__init__(
            master, 
            text=text,
            font= ("Arial", 22, "bold"),
            anchor="w", 
            text_color="black"
        )
