from sqlite3 import Connection

from darwin.models.backend_models import Teacher, TeacherId


class TeacherDal:

    def create_teacher(self, teacher: Teacher):
        ...

    def get_teacher(self, teacher_id: TeacherId): ...
