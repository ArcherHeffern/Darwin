
from datetime import datetime
from darwin.models.backend_models import (
    AssignmentId,
    BlobId,
    CourseId,
    ProjectType,
    SourceType,
)
from unittest import TestCase
from uuid import uuid4
from darwin.midtier.services.assignment import AssignmentService
from darwin.models.midtier_models import BasicAssignment, CreateAssignment, Assignment


class AssignmentTests(TestCase):

    def test_crud(self):

        course_id = CourseId(str(uuid4()))
        assignment_id = AssignmentId(str(uuid4()))

        create_assignment = CreateAssignment(
            id=assignment_id,
            course_f=course_id,
            name="PA 1",
            due_date=datetime(2024, 12, 4),
            project_type=ProjectType.MAVEN,
            source_type=SourceType.MOODLE,
            source_reference="",
            skeleton_f=BlobId("skeleton"),
            testfiles_f=BlobId("testfiles"),
        )

        expected_basic_assignments = [
            BasicAssignment(
                id=assignment_id,
                name=create_assignment.name,
                due_date=create_assignment.due_date,
            )
        ]

        expected_assignment = Assignment(
            id=assignment_id,
            course_f=course_id,
            name=create_assignment.name,
            due_date=create_assignment.due_date,
            project_type=create_assignment.project_type,
            source_type=create_assignment.source_type,
            source_reference=create_assignment.source_reference,
            skeleton_f=create_assignment.skeleton_f,
            testfiles_f=create_assignment.testfiles_f,
            last_downloaded=None,
        )


        AssignmentService.create(create_assignment)
        actual_basic_assignments = AssignmentService.get_all(course_id)
        self.assertEqual(actual_basic_assignments, expected_basic_assignments)

        actual_assignment = AssignmentService.get(assignment_id)
        self.assertEqual(actual_assignment, expected_assignment)