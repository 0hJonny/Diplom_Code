from fastapi import APIRouter

from controllers import ServiceController
from models import Task

router = APIRouter()

@router.post("/")
async def add_task(task: Task):
    controller = ServiceController()
    controller.add_task(task)
    return {"status": "task added"}

