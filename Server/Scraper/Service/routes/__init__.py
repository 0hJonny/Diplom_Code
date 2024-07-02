from fastapi import APIRouter

from routes import add_task, get_task, update_task

router = APIRouter()

router.include_router(add_task.router, prefix="/add_task", tags=["add_task"])
router.include_router(get_task.router, prefix="/get_task", tags=["get_task"])
router.include_router(update_task.router, prefix="/update_task", tags=["update_task"])
