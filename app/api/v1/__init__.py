from fastapi import APIRouter

from app.core.dependency import DependPermisson, DependDownloadTaskAuth

from .apis import apis_router
from .auditlog import auditlog_router
from .base import base_router
from .depts import depts_router
from .menus import menus_router
from .roles import roles_router
from .tasks import tasks_router
from .download_client import download_client_router
from .download_task import download_task_router

from .users import users_router

v1_router = APIRouter()

v1_router.include_router(base_router, prefix="/base")
v1_router.include_router(users_router, prefix="/user", dependencies=[DependPermisson])
v1_router.include_router(roles_router, prefix="/role", dependencies=[DependPermisson])
v1_router.include_router(menus_router, prefix="/menu", dependencies=[DependPermisson])
v1_router.include_router(tasks_router, prefix="/task", dependencies=[DependPermisson])
v1_router.include_router(download_client_router, prefix="/download/client", dependencies=[DependPermisson])
v1_router.include_router(download_task_router, prefix="/download/task", dependencies=[DependDownloadTaskAuth])
v1_router.include_router(download_task_router, prefix="/download/task", dependencies=[DependDownloadTaskAuth])
v1_router.include_router(apis_router, prefix="/api", dependencies=[DependPermisson])
v1_router.include_router(depts_router, prefix="/dept", dependencies=[DependPermisson])
v1_router.include_router(auditlog_router, prefix="/auditlog", dependencies=[DependPermisson])
