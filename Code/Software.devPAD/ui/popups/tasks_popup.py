import customtkinter as ctk

from backend.task_manager import TaskManager

class TasksPopup(ctk.CTkToplevel):

    def __init__(self, master):

        super().__init__(master)

        self.task_manager = TaskManager()
        self.title("Tasks")

        self.geometry("500x600")

        self.resizable(False, False)

        self.transient(master)

        self.grab_set()

        self.checkboxes = []

        self.build_ui()

    def build_ui(self):

        self.titleLabel = ctk.CTkLabel(
            self, 
            text="TASKS",

            font=("Arial", 28, "bold")
        )

        self.titleLabel.pack(
            pady=(20, 10)
        )

        self.progressLabel = ctk.CTkLabel(
            self, 
            text="0 / 0 complete", 
            font=("Arial", 15)
        )

        self.progressLabel.pack()

        self.listFrame = ctk.CTkScrollableFrame(
            self, 
            width=430,
            height=420
        )

        self.listFrame.pack(

            padx=20,
            pady=20,

            fill="both", 
            expand=True

        )

        self.bottomFrame = ctk.CTkFrame(
            self, 
            fg_color="transparent"
        )

        self.bottomFrame.pack(

            fill="x",
            padx=20, 
            pady=10
        )

        self.entry = ctk.CTkEntry(
            self.bottomFrame, 
            placeholder_text="New Task..."
        )

        self.entry.pack(

            side="left", 
            fill="x",
            expand=True, 
            padx=(0, 10)

        )

        self.entry.bind(
            "<Return>", 
            lambda e: self.add_task()
        )

        self.addButton = ctk.CTkButton(
            self.bottomFrame, 
            text="+", 
            width=45,
            command=self.add_task
        )

        self.addButton.pack(
            side="left"

        )

    def refresh_tasks(self):
        for widget in self.listFrame.winfo_children():
            widget.destroy()

        self.checkboxes.clear()

        tasks = self.task_manager.get_tasks()

        completed = 0

        for index, task in enumerate(tasks):
            if task["completed"]:
                completed += 1
            row = ctk.CTkFrame(
                self.listFrame,
                fg_color="transparent"
            )

            row.pack(
                fill="x",
                padx=5,
                pady=4
            )

            check = ctk.CTkCheckBox(
                row, 
                text=task["title"],
                command=lambda i=index: self.toggle_task(i)
            )

            if task["completed"]:
                check.select()

            check.pack(
                side="left",
                padx=(5, 10)
            )

            self.checkboxes.append(check)

            delete = ctk.CTkButton(

                row, 
                text="🗑",
                width=35,
                command=lambda i=index: self.delete_task(i)
            )


    def add_task(self):
        title = self.entry.get().strip()

        if title == "":
            return

        self.task_manager.add_task(title)

        self.entry.delete(0, "end")

        self.refresh_tasks()
    

    def toggle_task(self, index):
        self.task_manager.toggle_task(index)
        self.refresh_tasks()
    

    def delete_task(self, index):
        self.task_manager.delete_task(index)
        self.refresh_tasks()
