from sqlite3 import Connection


class TeacherCourseDal:
    def get_teacher_courses(self, teacher_id: int): ...
