from darwin.backend.dal.dal_I import Dal_I
from darwin.models.backend_models import Student as M_Student, StudentId, CourseId
from darwin.backend.schemas import Student as S_Student
from typing import Optional


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

    def maybe_get(self, student_id: StudentId) -> Optional[M_Student]:
        with self.db_session() as db:
            maybe_student = db.get(S_Student, student_id)
            if not maybe_student:
                return None
            return M_Student.model_validate(maybe_student)

    def get_all(
        self, course_id: Optional[CourseId] = None, hide_dropped: bool = True
    ) -> list[M_Student]:
        with self.db_session() as db:
            query = db.query(S_Student)
            if course_id:
                query = query.filter_by(course_f=course_id)
            if hide_dropped:
                query = query.filter_by(dropped=False)
            students = query.all()
            return [M_Student.model_validate(student) for student in students]
