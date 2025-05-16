from fastapi import APIRouter

from .sys_confs import router

confs_router = APIRouter()
confs_router.include_router(router, tags=["配置模块"])

__all__ = ["confs_router"]
