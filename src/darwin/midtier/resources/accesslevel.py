
from typing import Optional
from fastapi import APIRouter
from darwin.backend import Backend
from darwin.midtier.modules.authentication import ACCOUNT
from darwin.models.backend_models import AccessLevel, AccountPermission, ResourceId

resource_permission_dal = Backend.resource_permission_dal


router = APIRouter(
    prefix="/accesslevel",
    tags=["accesslevel"],
    responses={404: {"description": "Not found"}},
)

@router.get("/{resource_id}")
def get_access_level(account: ACCOUNT, resource_id: ResourceId) -> AccessLevel:
    if account.permission == AccountPermission.ADMIN:
        return AccessLevel.RD_WR_DEL
    resource_permission = resource_permission_dal.get(account.id, resource_id)
    if resource_permission is None:
        return AccessLevel.NONE
    return resource_permission.access_level