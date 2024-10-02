from sqlite3 import Connection
from uuid import uuid4

from models.backend_models import Teacher, TeacherId


class TeacherDal:
    def __init__(self, c: Connection):
        self.c = c

    def create_teacher(self, teacher: Teacher):
        c = self.c
        with c:
            c.execute(
                """
            --sql
            INSERT INTO teacher VALUES (?, ?, ?, ?);""",
                (teacher.id, teacher.account_f, teacher.course_f, teacher.resigned),
            )

    def get_teacher(self, teacher_id: TeacherId): ...
