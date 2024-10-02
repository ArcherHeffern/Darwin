from sqlite3 import Connection


class TeacherCourseDal:
    def __init__(self, c: Connection):
        self.c = c

    def assign_course_to_teacher(self, course_id: int, teacher_id: int):
        c = self.c
        with c:
            c.execute(
                """
            --sql
            INSERT INTO  
            ;
            """
            )

    def get_teacher_courses(self, teacher_id: int): ...
