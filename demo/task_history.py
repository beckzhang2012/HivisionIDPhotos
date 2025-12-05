import json
import os
from datetime import datetime


class TaskHistory:
    def __init__(self, history_file="task_history.json"):
        self.history_file = history_file
        self.history = self.load_history()

    def load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, "r") as f:
                return json.load(f)
        return []

    def save_history(self):
        with open(self.history_file, "w") as f:
            json.dump(self.history, f, indent=2, default=str)

    def add_task(self, task_id, file_name, status="Waiting", error=None):
        task = {
            "task_id": task_id,
            "file_name": file_name,
            "status": status,
            "error": error,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }
        self.history.append(task)
        self.save_history()
        return task

    def update_task(self, task_id, status, error=None):
        for task in self.history:
            if task["task_id"] == task_id:
                task["status"] = status
                task["error"] = error
                task["updated_at"] = datetime.now()
                self.save_history()
                return task
        return None

    def get_task(self, task_id):
        for task in self.history:
            if task["task_id"] == task_id:
                return task
        return None

    def get_all_tasks(self):
        return self.history

    def delete_task(self, task_id):
        for i, task in enumerate(self.history):
            if task["task_id"] == task_id:
                del self.history[i]
                self.save_history()
                return True
        return False
