from typing import Annotated, Optional
from fastapi import Depends, HTTPException, status
from darwin.midtier.modules.authentication.auth import get_auth_level
from darwin.models.backend_models import AccessLevel, AccountPermission
from darwin.models.midtier_models import Account, ResourceId
from darwin.backend import Backend

"""
Summary: 

AccountPermission: MEMBER, TA, TEACHER, ADMIN   # Mostly associated with resource creation
ResourcePermission: NONE, RD, RD_WR, RD_WR_DEL

"""
resource_permission_dal = Backend.resource_permission_dal

ACCOUNT = Annotated[Account, Depends(get_auth_level)]

def raise_if_not_admin(account: Account):
    if account.permission != AccountPermission.ADMIN:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

def raise_if_unauthorized_create(account: Account, min_req_permission: AccountPermission):
    if account.permission.value < min_req_permission.value:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
        
def raise_if_unauthorized_get(account: Account, resource: ResourceId):
    if account.permission is AccountPermission.ADMIN:
        return
    permission = resource_permission_dal.get(account.id, resource)
    if permission is None or permission.access_level == AccessLevel.NONE:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

def raise_if_unauthorized_modify(account: Account, resource: ResourceId):
    if account is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    if account.permission is AccountPermission.ADMIN:
        return
    permission = resource_permission_dal.get(account.id, resource)
    if permission is None or permission.access_level != AccessLevel.RD_WR:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)