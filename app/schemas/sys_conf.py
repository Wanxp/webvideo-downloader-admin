from pydantic import BaseModel
from tortoise.fields import Field



class BaseSysConf(BaseModel):
    id: int
    filePath: str

class SysConfCreate(BaseModel):
    filePath: str =  Field(example="../videos/")

class SysConfUpdate(BaseModel):
    id: int
    filePath: str = Field(example="../videos/")

