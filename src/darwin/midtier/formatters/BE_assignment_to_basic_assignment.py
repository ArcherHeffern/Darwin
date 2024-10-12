from darwin.models.backend_models import Assignment as BE_Assignment
from darwin.models.midtier_models import BasicAssignment

def BE_assignment_to_basic_assignment(BE_assignment: BE_Assignment) -> BasicAssignment:
    return BasicAssignment(
        id=BE_assignment.id, 
        name=BE_assignment.name, 
        due_date=BE_assignment.due_date,
    )