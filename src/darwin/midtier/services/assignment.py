from typing import Optional
from fastapi import HTTPException
from darwin.backend import Backend
from darwin.midtier.formatters.CreateAssignment_to_BE_Assignment import (
    createAssignment_to_BE_assignment,
)
from darwin.models.midtier_models import (
    BasicAssignment,
    Assignment as MT_Assignment,
    AssignmentId,
    CreateAssignment,
)
from darwin.models.backend_models import (
    Assignment as BE_Assignment,
    SourceType,
    CourseId,
)
from darwin.midtier.formatters.BE_assignment_to_basic_assignment import (
    BE_assignment_to_basic_assignment,
)
from darwin.backend import Backend
from darwin.midtier.formatters.BE_assignment_to_MT_assignment import (
    BE_assignment_to_MT_assignment,
)

assignment_dal = Backend.assignment_dal


class AssignmentService:

    @staticmethod
    def get(assignment_id: AssignmentId) -> MT_Assignment:
        BE_assignment = assignment_dal.get(assignment_id)
        if BE_assignment is None:
            raise HTTPException(404, "Assignment not found")
        return BE_assignment_to_MT_assignment(BE_assignment)

    @staticmethod
    def get_all(
        course_id: Optional[CourseId], hide_deleted: bool = True
    ) -> list[BasicAssignment]:
        BE_assignments = Backend.assignment_dal.get_all(course_id, hide_deleted)
        return [
            BE_assignment_to_basic_assignment(BE_assignment)
            for BE_assignment in BE_assignments
        ]

    @staticmethod
    def create(create_assignment: CreateAssignment) -> MT_Assignment:
        if (
            create_assignment.source_type == SourceType.MOODLE
            and create_assignment.id is None
        ):
            raise HTTPException(
                400, "Expected Assignment with MoodleSource to have assignmentId"
            )
        BE_assignment = createAssignment_to_BE_assignment(create_assignment)
        assignment_dal.create(BE_assignment)
        return BE_assignment_to_MT_assignment(BE_assignment)
