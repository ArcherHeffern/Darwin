from datetime import datetime
from darwin.models.backend_models import (
    Account,
    AccountId,
    AccountPermission,
    AccountStatus,
    Assignment,
    AssignmentId,
    BlobLocationType,
    CourseId,
    ProjectType,
    SourceType,
)
from unittest import TestCase
from uuid import uuid4
from darwin.backend import Backend


class AssignmentTests(TestCase):

    def test_crud(self):

        assignment: Assignment = Assignment(
            id=AssignmentId(int(uuid4())),
            course_f=CourseId(int(uuid4())),
            name="COSI 12b",
            due_date=datetime(2024, 12, 4),
            project_type_f=ProjectType.MAVEN,
            source_type=SourceType.MOODLE,
            source_reference="",
            assignment_stub_location_type_f=BlobLocationType.DISK,
            assignment_stub_reference="/home/moodle/assignment10",
            assignment_testfiles_location_type_f=BlobLocationType.DISK,
            assignment_testfiles_reference="/home/testfiles/assignment1",
            last_downloaded=datetime(2024, 12, 10, 12, 55),
            deleted=False,
        )

        Backend.assignment_dal.create(assignment)
