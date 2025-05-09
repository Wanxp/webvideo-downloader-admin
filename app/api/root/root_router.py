import json

from fastapi import APIRouter, Request

from app.controllers import task_controller
from app.schemas.tasks import DownloadTaskCreate

# router = APIRouter()
roott_router = APIRouter(tags=['下载任务'])

# 兼容 webvideo-downloader 版本
@roott_router.post(path="/", summary="新增下载任务")
async def create_download_task_for_local(
        request: Request
):
    body = await request.body()  # Read the raw body as bytes
    download_task_create_str = body.decode("utf-8")  # Decode bytes to string
    print(download_task_create_str)
    json_data = json.loads(download_task_create_str)  # Parse JSON string to dictionary
    download_task_create = DownloadTaskCreate(
        fileName=json_data.get("fileName"),
        pRange= json_data.get("pRange"),
        linksurl=json_data.get("linksurl"),
        data=json_data.get("data"),
        type=json_data.get("type"),
    )
    await task_controller.handle_create_task(download_task_create)
    return "success"

