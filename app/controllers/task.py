from datetime import datetime
from typing import Optional

from app.core.crud import CRUDBase
from app.downloader import download_queue
from app.downloader.api import getPlatformType
from app.models.task import Task
from app.schemas.tasks import TaskCreate, TaskUpdate, DownloadTaskCreate, StatusType


class TaskController(CRUDBase[Task, TaskCreate, TaskUpdate]):
    def __init__(self):
        super().__init__(model=Task)

    async def get_by_task_name(self, name: str) -> Optional["Task"]:
        return await self.model.filter(name=name).first()

    def build_task_create(self, download_task_create: DownloadTaskCreate) -> TaskCreate:
        taskCreate = TaskCreate(
            platform_type=getPlatformType(download_task_create.linksurl),
            quality='',
            totalSize=0,
            speed=0,
            rate=0,
            status=StatusType.WATING,
            order=int(datetime.now().timestamp()),
            # TODO fix this
            file_path='/home/wanxp/Downloads/webvideo/',
            parent_id=0,
            total=1,
            handled=0,
            fileName=download_task_create.fileName,
            pRange=download_task_create.pRange,
            linksurl=download_task_create.linksurl,
            data=download_task_create.data,
            type=download_task_create.type
        )
        return taskCreate

    async def handle_create_task(self, download_task_create: DownloadTaskCreate):
        task_create = self.build_task_create(download_task_create)
        await self.create(obj_in=task_create)
        task = await self.model.filter(fileName=task_create.fileName).filter(order=task_create.order).first()
        download_queue.put(task.to_dict())


task_controller = TaskController()
