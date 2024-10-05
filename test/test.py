from datetime import datetime
from src.darwin.models.backend_models import Account, AccountId, AccountPermission, AccountStatus, Assignment, AssignmentId, BlobLocationType, CourseId, ProjectType, SourceType
from unittest import TestCase
from uuid import uuid4
from src.darwin.backend.dal.dal import account_dal, assignment_dal


class AssignmentTests(TestCase):

    def test_crud(self):

        assignment: Assignment = Assignment(
            AssignmentId(int(uuid4())),
            CourseId(int(uuid4())),
            "COSI 12b",
            datetime(2024, 12, 4),
            ProjectType.MAVEN,
            SourceType.MOODLE,
            '',
            BlobLocationType.DISK,
            '/home/moodle/assignment10',
            BlobLocationType.DISK,
            '/home/testfiles/assignment1',
            datetime(2024, 12, 10, 12, 55),
            False
        )
        
class AccountTests(TestCase):
    def test_crud(self):
        account = Account(
            AccountId(2), "tim", "tim@gmail.com", "123", AccountStatus.UNREGISTERED, AccountPermission.ADMIN
        )
        account_dal.create_account(account)
        account_dal.get_account(AccountId(1))
        account_dal.get_account(AccountId(2))
