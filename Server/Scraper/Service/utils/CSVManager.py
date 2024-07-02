


from models import Task


class CSVManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.tasks = {}
        return cls._instance

    def read_tasks(self, path: str) -> dict:
        self.tasks = {}
        with open(path, "r") as file:
            lines = file.readlines()
            for line in lines:
                task_id, url = line.strip().split(",")
                self.tasks[task_id] = Task(task_id=task_id, url=url)
        return self.tasks

    def add_task(self, task: Task):
        self.tasks[task.task_id] = task
        with open("tasks.csv", "a") as file:
            file.write(f"{task.task_id},{task.url}\n")

    def delete_task(self, task_id: str):
        del self.tasks[task_id]
        with open("tasks.csv", "r") as file:
            lines = file.readlines()
        with open("tasks.csv", "w") as file:
            for line in lines:
                if task_id not in line:
                    file.write(line)

