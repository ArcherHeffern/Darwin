from darwin.models.backend_models import Assignment as BE_Assignment
from darwin.models.midtier_models import Assignment as MT_Assignment


def BE_assignment_to_MT_assignment(BE_assignment: BE_Assignment) -> MT_Assignment:
    return MT_Assignment(
        id=BE_assignment.id,
        course_f=BE_assignment.course_f,
        name=BE_assignment.name,
        due_date=BE_assignment.due_date,
        project_type=BE_assignment.project_type,
        source_type=BE_assignment.source_type,
        source_reference=BE_assignment.source_reference,
        skeleton_f=BE_assignment.skeleton_f,
        testfiles_f=BE_assignment.testfiles_f,
        last_downloaded=BE_assignment.last_downloaded,
    )
