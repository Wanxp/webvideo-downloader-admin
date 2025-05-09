from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Query

from app.schemas.base import Fail, Success
from app.controllers.download_client import download_client_controller

router = APIRouter()


@router.get("/get", summary="获取下载客户端")
async def get_download_client(
):
    downloader = await download_client_controller.get_download_client()
    downloader_dict = await downloader.to_dict()
    return Success(data=downloader_dict)

@router.post("/init", summary="初始化下载客户端")
async def create_download_client(
):
    downloader = await download_client_controller.init_download_client()
    downloader_dict = await downloader.to_dict()
    return Success(data=downloader_dict)

@router.delete("/delete", summary="删除下载客户端")
async def delete_download_client(
):
    await download_client_controller.remove_download_client()
    return Success(msg="Deleted Success")

