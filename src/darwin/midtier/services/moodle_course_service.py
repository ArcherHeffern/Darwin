from darwin.midtier.formatters.BE_teacher_to_MT_teacher import BE_teacher_to_MT_teacher
from darwin.models.midtier_models import Teacher as MT_Teacher, CourseId
from darwin.models.client_models import MoodleCourse
from darwin.backend import Backend
from darwin.midtier.formatters.moodle_course_to_BE_course import moodle_course_to_BE_course
from darwin.models.midtier_models import CourseGetBasic

def create(moodle_course: MoodleCourse) -> CourseGetBasic:
    course, accounts, students, tas, teachers = moodle_course_to_BE_course(moodle_course)

    Backend.course_dal.create(course)
    # If account with email exists - Ignore
    Backend.account_dal.try_create_all(accounts)
    Backend.student_dal.create_all(students)
    Backend.ta_dal.create_all(tas)
    Backend.teacher_dal.create_all(teachers)

    mt_teachers: list[MT_Teacher] = []
    for teacher in teachers:
        mt_teachers.append(BE_teacher_to_MT_teacher(teacher, accounts))

    return CourseGetBasic(
        id=course.id,
        name=course.name,
        teachers=mt_teachers,

    )

def get(self, course_id: CourseId):
    ...