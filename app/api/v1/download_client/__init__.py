from fastapi import APIRouter

from .download_client import router

download_client_router = APIRouter()
download_client_router.include_router(router, tags=["下载客户端模块"])

__all__ = ["download_client_router"]
