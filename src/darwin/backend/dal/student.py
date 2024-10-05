from src.darwin.models.backend_models import Student, StorageException
from sqlite3 import Connection


class StudentDal:
    def __init__(self, c: Connection):
        self.c: Connection = c

    def create_student(self, student: Student):
        """Creates student and returns course with id filled or raises StorageException"""
        c = self.c
        try:
            with c:
                c.execute(
                    """
                    --sql
                    INSERT INTO student (id, account_f, course_f, dropped) VALUES (?, ?, ?, ?);
                    """,
                    (student.id, student.account_f, student.course_f, student.dropped),
                )
            return student
        except Exception as e:
            raise StorageException(f"Failed to create student {student.id}: {e}")
