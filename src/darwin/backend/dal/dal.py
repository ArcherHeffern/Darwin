from sqlite3 import connect

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

DATABASE_PATH = 'db'

c = connect(DATABASE_PATH, timeout=5,  check_same_thread=False)
DbInit(c).create_database()


account_dal = AccountDal(c)
assignment_dal = AssignmentDal(c)
course_dal = CourseDal(c)
grading_metadata_dal = GradingMetadataDal(c)
non_passing_test_dal = NonPassingTestDal(c)
student_dal = StudentDal(c)
submission_dal = SubmissionDal(c)
ta_dal = TaDal(c)
teacher_course_dal = TeacherCourseDal(c)
teacher_dal = TeacherDal(c)
test_case_dal = TestCaseDal(c)
test_to_run_dal = TestToRunDal(c)
