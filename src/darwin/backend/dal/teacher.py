from sqlite3 import Connection
from typing import Optional

from darwin.backend.dal.dal_I import Dal_I
from darwin.models.backend_models import Teacher as M_Teacher, CourseId
from darwin.backend.schemas import Teacher as S_Teacher


class TeacherDal(Dal_I):

    def create(self, ta: M_Teacher):
        self.create_all([ta])

    def create_all(self, teachers: list[M_Teacher]):
        db_teachers: list[S_Teacher] = []
        for teacher in teachers:
            db_teacher = S_Teacher(
                id=teacher.id,
                account_f=teacher.account_f,
                course_f=teacher.course_f,
                resigned=teacher.resigned,
            )
            db_teachers.append(db_teacher)

        with self.db_session() as db:
            db.add_all(db_teachers)
            db.commit()

    def get_all(
        self, course_id: Optional[CourseId] = None, hide_dropped: bool = True
    ) -> list[M_Teacher]:
        with self.db_session() as db:
            query = db.query(S_Teacher)
            if course_id:
                query = query.filter_by(course_f=course_id)
            if hide_dropped:
                query = query.filter_by(resigned=False)
            teachers = query.all()
            return [M_Teacher.model_validate(teacher) for teacher in teachers]
