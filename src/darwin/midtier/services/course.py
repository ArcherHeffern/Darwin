from darwin.backend import Backend
from darwin.models.midtier_models import BasicCourse as MT_BasicCourse, CourseId
from darwin.models.backend_models import Course as BE_Course, AccountId
from itertools import chain

course_dal = Backend.course_dal
teacher_dal = Backend.teacher_dal

"""
============
Accepts Midtier model, decomposes into multiple backend models, and creates them using the DAL
============
"""


class CourseService:
    # @staticmethod
    # def create(course: M_Course) -> MT_Course:
    #     course_dal.create(course)

    @staticmethod
    def get_all_basic(account_id: AccountId) -> list[MT_BasicCourse]:
        student_courses: list[BE_Course] = course_dal.get_student_courses_by_account(account_id)
        ta_courses: list[BE_Course] = course_dal.get_ta_courses_by_account(account_id)
        teacher_courses: list[BE_Course] = course_dal.get_teacher_courses_by_account(account_id)

        courses: list[MT_BasicCourse] = []
        seen_ids: set[CourseId] = set()
        for BE_course in chain(student_courses, ta_courses, teacher_courses):
            if BE_course.id in seen_ids:
                continue
            seen_ids.add(BE_course.id)
            course = MT_BasicCourse(id=BE_course.id, name=BE_course.name)
            courses.append(course)

        return courses

if __name__ == '__main__':
    print(CourseService.get_all_basic(AccountId('8ee9f255-6515-4184-a71d-b481ad1a9a25')))
    print(CourseService.get_all_basic(AccountId('kjdsfkj')))
