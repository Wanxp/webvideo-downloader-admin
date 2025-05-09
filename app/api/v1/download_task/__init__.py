from fastapi import APIRouter

from .download_task import router


download_task_router = APIRouter()
download_task_router.include_router(router, tags=["下载任务模块"])

__all__ = [ "download_task_router"]
