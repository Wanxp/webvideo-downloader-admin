from datetime import datetime
from email.policy import default

from tortoise import fields

from app.schemas.menus import MenuType

from .base import BaseModel, TimestampMixin
from ..schemas.tasks import PlatformType, StatusType, UrlStatusType


class Task(BaseModel, TimestampMixin):
    platform_type = fields.CharEnumField(PlatformType,  description="平台", index=True)
    quality = fields.CharField(max_length=100, null=True, description="画质")
    totalSize = fields.IntField(default=0, description="大小")
    currentSize= fields.IntField(default=0, description="当前大小")
    speed = fields.IntField(default=0, description="速度")
    rate = fields.FloatField(default=0.0, description="进度")
    status = fields.IntEnumField(StatusType,  description="状态", index=True)
    order = fields.IntField(default=0, description="排序", index=True)
    file_path = fields.CharField(max_length=20000, description="本地路径")
    parent_id = fields.IntField(default=0, description="父菜单ID", index=True)
    total = fields.IntField(default=1, description="总数量")
    handled = fields.IntField(default=0, description="已处理数量")
    fileName: str = fields.CharField(max_length=20000, description="文件名称", index=True)
    pRange: str = fields.CharField(max_length=2000, description="P范围", null=True)
    linksurl: str = fields.CharField(max_length=20000, description="关联地址", null=True)
    data: str = fields.CharField(max_length=20000, description="数据信息", null=True)
    type: str = fields.CharField(max_length=200, description="地址类型", null=True)
    url_status = fields.IntEnumField(UrlStatusType, description="地址状态", null=True)
    class Meta:
        table = "task"



    def to_dict(self, m2m: bool = False, exclude_fields: list[str] | None = None):
        """
        将模型转换为字典
        :param m2m: 是否包含多对多关系
        :param exclude_fields: 排除的字段
        :return: 字典
        """
        data = {}
        data["id"] = self.id
        data["created_at"] = self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at
        data["updated_at"] = self.updated_at.isoformat() if isinstance(self.updated_at, datetime) else self.updated_at
        data["platform"] = self.platform_type.name

        data["platform_type"] = self.platform_type.value
        data["quality"] = self.quality
        data["totalSize"] = self.totalSize
        data["currentSize"] = self.currentSize
        data["speed"] = self.speed
        data["rate"] = self.rate
        data["status"] = self.status.value
        data["order"] = self.order
        data["file_path"] = self.file_path
        data["parent_id"] = self.parent_id
        data["total"] = self.total
        data["handled"] = self.handled
        data["fileName"] = self.fileName
        data["pRange"] = self.pRange
        data["linksurl"] = self.linksurl
        data["data"] = self.data
        data["type"] = self.type
        data["url_status"] = self.url_status.value if self.url_status else None
        return data

class DownloadClient(BaseModel, TimestampMixin):
    name = fields.CharField(max_length=2000, description="名称", index=True)
    token = fields.CharField(max_length=512, description="鉴权", index=True)
    class Meta:
        table = "download_client"

class TaskDownloadSpeed(BaseModel, TimestampMixin):
    startTime = fields.DatetimeField(null=True, description="开始时间")
    totalSize = fields.IntField(default=0, description="大小")
    currentSize = fields.IntField(default=0, description="当前大小")
    speed = fields.IntField(default=0, description="速度")
    taskId = fields.IntField(default=0, description="任务ID", index=True)

    class Meta:
        table = "task"