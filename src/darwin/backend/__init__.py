from darwin.models.backend_models import Course, CourseId
import darwin.backend.schemas as schemas
from darwin.backend.db_init import engine, SessionLocal
from darwin.backend.dal.account import AccountDal
from darwin.backend.dal.assignment import AssignmentDal
from darwin.backend.dal.course import CourseDal
from darwin.backend.dal.grading_metadata import GradingMetadataDal
from darwin.backend.dal.non_passing_test import NonPassingTestDal
from darwin.backend.dal.student import StudentDal
from darwin.backend.dal.submission import SubmissionDal
from darwin.backend.dal.ta import TaDal
from darwin.backend.dal.teacher_course import TeacherCourseDal
from darwin.backend.dal.teacher import TeacherDal
from darwin.backend.dal.test_case import TestCaseDal
from darwin.backend.dal.test_to_run import TestToRunDal
from config import Config

# TODO: Grading config used by assignment for grading
# TODO: Notification system
# TODO: Logging system
# TODO: Permissions table


class _Backend:
    def __init__(self):
        # Create database
        schemas.Base.metadata.create_all(bind=engine)

        self.account_dal = AccountDal(SessionLocal)
        self.assignment_dal = AssignmentDal(SessionLocal)
        self.course_dal = CourseDal(SessionLocal)
        self.grading_metadata_dal = GradingMetadataDal()
        self.non_passing_test_dal = NonPassingTestDal()
        self.student_dal = StudentDal(SessionLocal)
        self.submission_dal = SubmissionDal()
        self.ta_dal = TaDal(SessionLocal)
        self.teacher_course_dal = TeacherCourseDal()
        self.teacher_dal = TeacherDal(SessionLocal)
        self.test_case_dal = TestCaseDal()
        self.test_to_run_dal = TestToRunDal()


Backend: _Backend = _Backend()

if Config.DB_DATA:
    from darwin.backend.mock_data import MockData

    MockData.create()

if __name__ == "__main__":
    course = Backend.course_dal.get(CourseId("0"))
    courses = Backend.course_dal.get_all()
    print([course.name for course in courses])
