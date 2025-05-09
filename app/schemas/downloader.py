from enum import StrEnum, IntEnum
from typing import Optional

from pydantic import BaseModel, Field



class BaseDownloadClient(BaseModel):
    id: int
    name: str
    token: str


class DownloadClientCreate(BaseModel):
    id: int = Field(example=1)
    name: str = Field(example="油猴脚本")
    token: str = Field(example="HjyhtQhevMlTKZQ2M0IgIEYoeVbFcoAB9tgLazscaOWCpTOmbPlkHFSs")

class DownloadClientUpdate(BaseModel):
    id: int
    name: str = Field(example="油猴脚本")
    token: str = Field(example="HjyhtQhevMlTKZQ2M0IgIEYoeVbFcoAB9tgLazscaOWCpTOmbPlkHFSs")


