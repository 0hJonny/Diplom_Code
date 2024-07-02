from fastapi import APIRouter
from controllers import ServiceController
from models import Article

router = APIRouter()

@router.post("/")
def update_task(task_id: str, status: str, article: Article = None):
    controller = ServiceController()
    controller.update_task_status(task_id, status, article)
    return {"message": "Task updated successfully", "task_id": task_id, "status": status}