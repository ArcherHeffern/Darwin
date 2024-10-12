from datetime import datetime
from darwin.models.backend_models import (
    Assignment,
    BlobId,
    AssignmentId,
    CourseId,
    ProjectType,
    SourceType,
)
from unittest import TestCase
from uuid import uuid4
from darwin.backend import Backend


class AssignmentTests(TestCase):

    def test_crud(self):

        expected_assignment: Assignment = Assignment(
            id=AssignmentId(str(uuid4())),
            course_f=CourseId(str(uuid4())),
            name="COSI 12b",
            due_date=datetime(2024, 12, 4),
            project_type=ProjectType.MAVEN,
            source_type=SourceType.MOODLE,
            source_reference="",
            skeleton_f=BlobId("skeleton"),
            testfiles_f=BlobId("testfiles"),
            last_downloaded=datetime(2024, 12, 10, 12, 55),
            deleted=False,
        )

        Backend.assignment_dal.create(expected_assignment)
        maybe_actual_assignment: Assignment | None = Backend.assignment_dal.get(
            expected_assignment.id
        )
        self.assertIsNotNone(maybe_actual_assignment)
        actual_assignment: Assignment = maybe_actual_assignment  # type: ignore
        self.assertEqual(actual_assignment, expected_assignment)
        self.assertEqual(actual_assignment.id, expected_assignment.id)
        self.assertEqual(actual_assignment.due_date, expected_assignment.due_date)
