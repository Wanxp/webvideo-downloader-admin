from tortoise import fields

from app.models import BaseModel, TimestampMixin


class SysConf(BaseModel, TimestampMixin):
    filePath = fields.CharField(max_length=10000, null=True, description="文件路径")
    class Meta:
        table = "sys_conf"


