from fastapi import APIRouter, HTTPException

from controllers import ServiceController

router = APIRouter()

@router.get("/")
async def get_task():
    controller = ServiceController()
    task = controller.get_task()
    if task:
        return task
    raise HTTPException(status_code=204, detail="no tasks")
