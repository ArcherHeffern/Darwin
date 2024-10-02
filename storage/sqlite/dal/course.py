from sqlite3 import Connection
from models.backend_models import Course, StorageException

"""

Does not do any business logic

"""


class CourseDal:
    def __init__(self, c: Connection):
        self.c = c

    def create_course(self, course: Course):
        """Raises exception on failure"""
        c = self.c
        with c:
            c.execute(
                """
                      --sql
                      INSERT INTO course (id, name, deleted) VALUES (?, ?, FALSE)
                      ;""",
                (course.id, course.name),
            )
