from sqlite3 import Connection

from darwin.backend.dal.dal_I import Dal_I
from darwin.models.backend_models import Teacher as M_Teacher, TeacherId
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
