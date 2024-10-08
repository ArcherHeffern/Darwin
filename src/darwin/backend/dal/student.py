from darwin.backend.dal.dal_I import Dal_I
from darwin.models.backend_models import Student as M_Student
from darwin.backend.schemas import Student as S_Student


class StudentDal(Dal_I): 
    def create(self, student: M_Student):
        self.create_all([student])

    def create_all(self, students: list[M_Student]):
        db_students: list[S_Student] = []
        for student in students:
            db_student = S_Student(
                id=student.id,
                account_f=student.account_f,
                course_f=student.course_f,
                dropped=student.dropped,
            )
            db_students.append(db_student)

        with self.db_session() as db:
            db.add_all(db_students)
            db.commit()
