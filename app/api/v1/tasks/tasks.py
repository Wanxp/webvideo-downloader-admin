import logging

from fastapi import APIRouter, Query
from tortoise.expressions import Q
from app.controllers.task import task_controller

from app.schemas.base import Fail, Success, SuccessExtra

from app.schemas.tasks import *

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/list", summary="查看任务列表")
async def list_task(
    page: int = Query(1, description="页码"),
    page_size: int = Query(10, description="每页数量"),
    fileName: str = Query("", description="文件名称"),
    platform_type: str = Query("", description="平台类型"),
    status: int = Query("", description="任务状态"),
):
    async def get_task_with_children(task_id: int):
        task = await task_controller.model.get(id=task_id)
        task_dict = task.to_dict()
        child_tasks = await task_controller.model.filter(parent_id=task_id).order_by("order")
        task_dict["children"] = [await get_task_with_children(child.id) for child in child_tasks]
        return task_dict

    q = Q()
    q &= Q(parent_id=0)
    if fileName:
        q &= Q(fileName=fileName)
    if platform_type:
        q &= Q(platform_type=platform_type)
    if status:
        q &= Q(status=status)

    total, parent_tasks = await task_controller.list(page=page, page_size=page_size, search=q, order=["order", "id"])

    res_task = [await get_task_with_children(task.id) for task in parent_tasks]
    return SuccessExtra(data=res_task, total=total, page=page, page_size=page_size)


@router.get("/get", summary="查看任务")
async def get_task(
    task_id: int = Query(..., description="任务id"),
):
    result = await task_controller.get(id=task_id)
    result_dict = await result.to_dict()
    return Success(data=result_dict)


@router.post("/create", summary="创建任务")
async def create_task(
    task_in: TaskCreate,
):
    await task_controller.create(obj_in=task_in)
    return Success(msg="Created Success")


@router.post("/update", summary="更新任务")
async def update_task(
    task_in: TaskUpdate,
):
    await task_controller.update(id=task_in.id, obj_in=task_in)
    return Success(msg="Updated Success")


@router.delete("/delete", summary="删除任务")
async def delete_task(
    id: int = Query(..., description="任务id"),
):
    child_task_count = await task_controller.model.filter(parent_id=id).count()
    if child_task_count > 0:
        return Fail(msg="Cannot delete a task with child tasks")
    await task_controller.remove(id=id)
    return Success(msg="Deleted Success")


