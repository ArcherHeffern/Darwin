from ..dal.dal import assignment_dal as assignment

class AssignmentService:
    def __init__(self):
        ...

    def get_assignments(self):
        return assignment.get_all()