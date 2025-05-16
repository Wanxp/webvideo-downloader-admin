import logging

from fastapi import APIRouter, Query
from app.controllers.sys_conf import sys_conf_controller

from app.schemas.base import Fail, Success, SuccessExtra

from app.schemas.sys_conf import *

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/get", summary="查看配置")
async def get_conf():
    result = await sys_conf_controller.get(id=1)
    if not result:
        sys_conf_controller.create(SysConfCreate(
            filePath="../videos/",
        ))
    result_dict = await result.to_dict()
    return Success(data=result_dict)

@router.post("/update", summary="更新配置")
async def update_conf(
    conf_in: SysConfUpdate,
):
    await sys_conf_controller.update(id=conf_in.id, obj_in=conf_in)
    return Success(msg="Updated Success")

