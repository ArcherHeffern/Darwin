from sqlite3 import connect, Connection
from pathlib import Path
from typing import Self

from ..db_init import DbInit
from .account import AccountDal
from .assignment import AssignmentDal
from .course import CourseDal
from .grading_metadata import GradingMetadataDal
from .non_passing_test import NonPassingTestDal
from .student import StudentDal
from .submission import SubmissionDal
from .ta import TaDal
from .teacher_course import TeacherCourseDal
from .teacher import TeacherDal
from .test_case import TestCaseDal
from .test_to_run import TestToRunDal

# TODO: Grading config used by assignment for grading
# TODO: Notification system
# TODO: Logging system
# TODO: Permissions table


class SQLiteStorage:

    def __init__(self, c: Connection):
        self.c = c
        DbInit(c).create_database()
        self.account_dal = AccountDal(c)
        self.course_dal = CourseDal(c)
        self.grading_metadata_dal = GradingMetadataDal(c)
        self.non_passing_test_dal = NonPassingTestDal(c)
        self.student_dal = StudentDal(c)
        self.submission_dal = SubmissionDal(c)
        self.ta_dal = TaDal(c)
        self.teacher_course_dal = TeacherCourseDal(c)
        self.teacher_dal = TeacherDal(c)
        self.test_case_dal = TestCaseDal(c)
        self.test_to_run_dal = TestToRunDal(c)

    @classmethod
    def connect(cls, database_path: Path) -> Self:
        con = connect(database_path, timeout=5)
        return cls(con)

    def disconnect(self):
        self.c.close()

    @classmethod
    def __register_adapters(cls, c: Connection): ...

    @classmethod
    def __register_converters(cls, c: Connection): ...
