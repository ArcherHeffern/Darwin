from typing import Optional
from darwin.backend.dal.dal_I import Dal_I
from darwin.models.backend_models import (
    AccountId,
    ResourceId,
    ResourcePermission as M_ResourcePermission,
)
from darwin.backend.schemas import ResourcePermission as S_ResourcePermission


class ResourcePermissionDal(Dal_I):
    def get(
        self, account_id: AccountId, resource_id: ResourceId
    ) -> Optional[M_ResourcePermission]:
        with self.db_session() as db:
            resource_permission = (
                db.query(S_ResourcePermission)
                .filter_by(account_id=account_id, resource_id=resource_id)
                .one_or_none()
            )
            if resource_permission is None:
                return None
            return M_ResourcePermission.model_validate(resource_permission)

    def create(self, resource_permission: M_ResourcePermission):
        with self.db_session() as db:
            db_resource_permission = S_ResourcePermission(
                account_id=resource_permission.account_id,
                resource_id=resource_permission.resource_id,
                access_level=resource_permission.access_level,
            )
            db.add(db_resource_permission)
