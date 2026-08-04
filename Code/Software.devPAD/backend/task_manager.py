from pathlib import Path
import json

class TaskManager:
    def __init__(self):

        self.file = (
            Path(__file__).resolve().parents[1]
            /"tasks.json"
        )

        if not self.file.exists():
            self._create_default()

        self.load()

    def _create_default(self):

        self.data = {
            "tasks": []
        }
        self.save()

    def load(self):
        with open (self.file, "r", encoding="utf8") as f:
            self.data = json.load(f)
        self.data.setdefault("tasks", [])

    def save(self):

        with open(self.file, "w", encoding="utf8") as f:
            json.dump(
                self.data, 
                f, 
                indent=4
            )
    def get_tasks(self):

        return self.data["tasks"]

    def add_task(self, title):

        title = title.strip()

        if title == "":
            return
        self.data["tasks"].append({

            "title": title, 
            "completed": False
        })

        self.save

    def toggle_task(self, index):

        if 0 <= index < len(self.data["tasks"]):
            task = self.data["tasks"][index]
            task["completed"] = not task["completed"]

            self.save

    def update_title(self, index, title):

          if 0 <= index < len(self.data["tasks"]):

              self.data["tasks"][index]["title"] = title

              self.save()

    def clear_completed(self):

        self.data["tasks"] = [

            t for t in self.data["tasks"]

            if not t["completed"]

        ]

        self.save()

    def delete_task(self, index):

        if 0 <= index < len(self.data["tasks"]):   
             self.data["tasks"].pop(index)

             self.save()