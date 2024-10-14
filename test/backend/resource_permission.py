from datetime import datetime
from darwin.models.backend_models import (
    AccessLevel,
    AccountId,
    CourseId,
    ResourcePermission,
    ResourcePermissionId,
)
from unittest import TestCase
from darwin.backend import Backend

resource_permission_dal = Backend.resource_permission_dal


class ResourcePermissionTests(TestCase):

    def test_crud(self):
        expected_resource_permission = ResourcePermission(
            account_id=AccountId("0"),
            resource_id=CourseId("305"),
            access_level=AccessLevel.RD,
        )
        resource_permission_dal.create(expected_resource_permission)
        actual_resource_permission = resource_permission_dal.get(
            expected_resource_permission.account_id,
            expected_resource_permission.resource_id,
        )

        self.assertEqual(actual_resource_permission, expected_resource_permission)
