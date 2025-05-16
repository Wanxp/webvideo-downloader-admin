from app.core.crud import CRUDBase

from app.models.sys_conf import SysConf
from app.schemas.sys_conf import SysConfCreate, SysConfUpdate


class SysConfController(CRUDBase[SysConf, SysConfCreate, SysConfUpdate]):
    def __init__(self):
        super().__init__(model=SysConf)

sys_conf_controller = SysConfController()
