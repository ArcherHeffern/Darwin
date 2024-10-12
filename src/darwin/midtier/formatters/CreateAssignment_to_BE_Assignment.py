from darwin.models.midtier_models import CreateAssignment
from darwin.models.backend_models import Assignment as BE_Assignment, AssignmentId
from uuid import uuid4


def createAssignment_to_BE_assignment(
    create_assignment: CreateAssignment,
) -> BE_Assignment:
    """
    Assigns assignmentId a uuid if it does not exist
    """
    return BE_Assignment(
        id=create_assignment.id or AssignmentId(str(uuid4())),
        name=create_assignment.name,
        course_f=create_assignment.course_f,
        due_date=create_assignment.due_date,
        project_type=create_assignment.project_type,
        source_type=create_assignment.source_type,
        source_reference=create_assignment.source_reference,
        skeleton_f=create_assignment.skeleton_f,
        testfiles_f=create_assignment.testfiles_f,
        last_downloaded=None,
        deleted=False,
    )
