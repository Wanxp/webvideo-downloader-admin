from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Query

from app.schemas.base import Fail, Success
from app.controllers.download_client import download_client_controller
from app.schemas.tasks import DownloadTaskCreate

router = APIRouter()




@router.post("/create", summary="新增下载")
async def create_download_task(
    download_task_create: DownloadTaskCreate,
):
    downloader = await download_client_controller.handle_create_task(download_task_create)
    downloader_dict = await downloader.to_dict()
    return Success(data=downloader_dict)

