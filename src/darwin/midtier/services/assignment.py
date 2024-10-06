from darwin.backend import Backend
from darwin.models.backend_models import Assignment


class AssignmentService:

    @staticmethod
    def get_all() -> list[Assignment]:
        return Backend.assignment_dal.get_all()
