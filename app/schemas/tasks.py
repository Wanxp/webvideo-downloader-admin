from enum import StrEnum, IntEnum
from typing import Optional

from pydantic import BaseModel, Field


class PlatformType(StrEnum):
    BILI = "bili"  # 哔哩
    IQIYI = "爱奇艺"  # 菜单
    VQQ = "vqq"  # 腾讯
    MGTV = "mgtv"  # 芒果
    WETV = "wetv"  # WeTV
    IQ = "iq"  # 爱奇艺(国际)
    UNKNOWN = "unknown"


class StatusType(IntEnum):
    WATING = 10  # 等待下载
    DOING = 20  # 下载中
    MERGING = 30  # 合并中
    DONE = 40  # 下载完成
    STOP = 99  # 停止
    PAUSE = 199  # 暂停

class UrlStatusType(IntEnum):
    OK = 0  # 正常
    ERROR = 1  # 错误
    TIMEOUT = 2  # 超时
    NOT_FOUND = 3  # 找不到
    INVALID = 4  # 无效链接


class BaseMenu(BaseModel):
    id: int
    platform_type: Optional[PlatformType]
    quality: Optional[str]
    totalSize: Optional[int]
    currentSize: Optional[int]
    speed: Optional[int]
    rate: Optional[float]
    status: StatusType
    parent_id: Optional[int]
    file_path: str
    total: int
    handled: int
    order: int
    fileName: str
    pRange: Optional[str]
    linksurl: str
    data: str
    type: str
    url_status: UrlStatusType

class TaskCreate(BaseModel):
    platform_type: Optional[PlatformType] = Field(example=PlatformType.BILI.value)
    quality: Optional[str] = "1080p"
    totalSize: Optional[int] = 0
    currentSize: Optional[int] = 0
    speed: Optional[int] = 0
    rate: Optional[float] = 0.0
    status: StatusType = Field(example=StatusType.WATING)
    parent_id: Optional[int] = Field(example=1)
    file_path: str = Field(example="./我的文件")
    order: int = Field(example=1)
    total: int = Field(example=1)
    handled: int = Field(example=0)
    fileName: str = Field(example="我的文件")
    pRange: Optional[str] = Field(example="1 2")
    linksurl: str = Field(example="https://www.bilibili.com/video/BV1xE411D7nM")
    data: str = Field(example="{}")
    type: str = Field(example="link")
    url_status: Optional[UrlStatusType] = Field(example=UrlStatusType.OK.value)

class TaskUpdate(BaseModel):
    id: int
    # platform_type: Optional[PlatformType] = Field(example=PlatformType.BILI.value)
    quality: Optional[str] = "1080p"
    totalSize: Optional[int] = 0
    currentSize: Optional[int] = 0
    speed: Optional[int] = 0
    rate: Optional[float] = 0.0
    status: StatusType = Field(example=StatusType.WATING)
    # parent_id: Optional[int] = Field(example=1)
    file_path: str = Field(example="./我的文件")
    # order: int = Field(example=1)
    total: int = Field(example=1)
    handled: int = Field(example=0)
    fileName: str = Field(example="我的文件")
    # pRange: Optional[str] = Field(example="1 2")
    # linksurl: str = Field(example="https://www.bilibili.com/video/BV1xE411D7nM")
    # data: str = Field(example="{}")
    # type: str = Field(example="link")
    url_status: Optional[UrlStatusType] = Field(example=UrlStatusType.OK.value)



class DownloadTaskCreate(BaseModel):
    fileName: str = Field(example="我的文件")
    pRange: Optional[str] = Field(example="1 2")
    linksurl: str = Field(example="https://www.bilibili.com/video/BV1xE411D7nM")
    data: str = Field(example="{}")
    type: str = Field(example="link")


class DispatchedTask(object):
    def __init__(self, id:int, pRange:str, isSubTask:bool = False):
        self.id = id
        self.pRange = pRange
        self.isSubTask = isSubTask