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

# TODO: Grading config used by assignment for grading
# TODO: Notification system
# TODO: Logging system
# TODO: Permissions table

class _Dal:
    DATABASE_PATH = 'db'

    def __init__(self):
        schemas.Base.metadata.create_all(bind=engine)
        self.__session_maker = SessionLocal

        self.account_dal = AccountDal()
        self.assignment_dal = AssignmentDal()
        self.course_dal = CourseDal(self.__session_maker)
        self.grading_metadata_dal = GradingMetadataDal()
        self.non_passing_test_dal = NonPassingTestDal()
        self.student_dal = StudentDal()
        self.submission_dal = SubmissionDal()
        self.ta_dal = TaDal()
        self.teacher_course_dal = TeacherCourseDal()
        self.teacher_dal = TeacherDal()
        self.test_case_dal = TestCaseDal()
        self.test_to_run_dal = TestToRunDal()
    
    def create_session(self):
        return self.__SessionLocal()


Dal = _Dal()
if __name__ == '__main__':
    # course = Course(id = CourseId(0), name = "COSI 12b", deleted = False)
    # Dal.course_dal.create(course)
    course = Dal.course_dal.get(CourseId(0))
    courses = Dal.course_dal.get_all()
    print([course.name for course in courses])