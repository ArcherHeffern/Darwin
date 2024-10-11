from darwin.midtier.formatters.BE_teacher_to_MT_teacher import BE_teacher_to_MT_teacher
from darwin.models.midtier_models import (
    Student as MT_Student,
    Teacher as MT_Teacher,
    CourseId,
    Ta as MT_Ta,
)
from darwin.models.client_models import MoodleCourse
from darwin.backend import Backend
from darwin.midtier.formatters.moodle_course_to_BE_course import (
    moodle_course_to_BE_course,
)
from darwin.models.midtier_models import Course


def create(moodle_course: MoodleCourse) -> Course:
    course, accounts, students, tas, teachers = moodle_course_to_BE_course(
        moodle_course
    )

    Backend.course_dal.create(course)
    # If account with email exists - Ignore
    Backend.account_dal.try_create_all(accounts)
    Backend.student_dal.create_all(students)
    Backend.ta_dal.create_all(tas)
    Backend.teacher_dal.create_all(teachers)

    account_lookup = {a.id: a for a in accounts}
    mt_students: list[MT_Student] = []
    mt_tas: list[MT_Ta] = []
    mt_teachers: list[MT_Teacher] = []

    for student in students:
        mt_students.append(
            MT_Student(
                id=student.id,
                name=account_lookup[student.account_f].name,
                email=account_lookup[student.account_f].email,
            )
        )
    for ta in tas:
        mt_tas.append(
            MT_Ta(
                id=ta.id,
                name=account_lookup[ta.account_f].name,
                email=account_lookup[ta.account_f].email,
            )
        )
    for teacher in teachers:
        mt_teachers.append(
            MT_Teacher(
                id=teacher.id,
                name=account_lookup[teacher.account_f].name,
                email=account_lookup[teacher.account_f].email,
            )
        )

    return Course(
        id=course.id,
        name=course.name,
        teachers=mt_teachers,
        tas=mt_tas,
        students=mt_students,
        assignments=[],
    )


def get(self, course_id: CourseId): ...
