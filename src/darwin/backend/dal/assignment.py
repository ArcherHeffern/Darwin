from typing import Optional
from sqlalchemy.orm import Session

from darwin.backend.dal.dal_I import Dal_I
from darwin.backend.schemas import Assignment as S_Assignment
from darwin.models.backend_models import (
    Assignment as M_Assignment,
    AssignmentId,
    CourseId,
)


class AssignmentDal(Dal_I):

    def get(self, assignment_id: AssignmentId) -> Optional[M_Assignment]:
        with self.db_session() as db:
            maybe_assignment = db.get(S_Assignment, assignment_id)
            if maybe_assignment is None:
                return None
            return M_Assignment.model_validate(maybe_assignment)

    def get_all(
        self, course_id: Optional[CourseId] = None, hide_deleted: bool = True
    ) -> list[M_Assignment]:
        with self.db_session() as db:
            query = db.query(S_Assignment)
            if hide_deleted:
                query = query.filter_by(deleted=False)
            if course_id is not None:
                query = query.filter_by(course_f=course_id)
        assignments = query.all()
        return [M_Assignment.model_validate(assignment) for assignment in assignments]

    def create(self, assignment: M_Assignment):
        with self.db_session() as db:
            db_assignment = S_Assignment(
                id=assignment.id,
                course_f=assignment.course_f,
                name=assignment.name,
                due_date=assignment.due_date,
                project_type=assignment.project_type,
                source_type=assignment.source_type,
                source_reference=assignment.source_reference,
                skeleton_f=assignment.skeleton_f,
                testfiles_f=assignment.testfiles_f,
                last_downloaded=assignment.last_downloaded,
                deleted=assignment.deleted,
            )
            db.add(db_assignment)
