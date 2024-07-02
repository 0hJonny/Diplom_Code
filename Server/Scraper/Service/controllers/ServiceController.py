
import queue
import threading

from models import Article, Task


class ServiceController:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ServiceController, cls).__new__(cls)
            cls._instance.task_queue = queue.Queue()
            cls._instance.tasks = {}
            cls._instance.lock = threading.Lock()
        return cls._instance

    def add_task(self, task: Task):
        with self.lock:
            self.tasks[task.task_id] = task
            self.task_queue.put(task.task_id)

    def get_task(self) -> Task:
        try:
            task_id = self.task_queue.get(timeout=5)
            return self.tasks[task_id]
        except queue.Empty:
            return None

    def update_task_status(self, task_id: str, status: str, article: Article = None):
        with self.lock:
            if task_id in self.tasks:
                task = self.tasks[task_id]
                task.status = status
                task.article = article
                if status in ["completed", "failed"]:
                    del self.tasks[task_id]
