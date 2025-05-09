import json
from datetime import datetime
from typing import Optional

from app.core.crud import CRUDBase
from app.downloader import download_queue
from app.downloader.api import getPlatformType
from app.models.task import  DownloadClient
from app.schemas.downloader import  DownloadClientCreate, DownloadClientUpdate
from app.schemas.tasks import DownloadTaskCreate, TaskCreate, StatusType
from app.utils.string_util import generate_random_str


class DownloadClientController(CRUDBase[DownloadClient, DownloadClientCreate, DownloadClientUpdate]):
    def __init__(self):
        super().__init__(model=DownloadClient)

    async def get_download_client(self) -> Optional[DownloadClient]:
        return await self.model.filter(id=1).first()

    async def init_download_client(self) -> Optional[DownloadClient]:
        downloader = await self.model.filter(id=1).first()
        if downloader is None:
            download_client_create = DownloadClientCreate(id=1, name="油猴脚本", token=generate_random_str(128))
            await self.create(obj_in=download_client_create)
            downloader = await self.model.filter(id=1).first()
        return downloader


    async def remove_download_client(self) :
        return await self.remove(id=1)






download_client_controller = DownloadClientController()
