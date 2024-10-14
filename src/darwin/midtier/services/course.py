from typing import Optional
from fastapi import HTTPException, status
from darwin.backend import Backend
from darwin.midtier.clients.moodle.moodle_client import MoodleClient
from darwin.midtier.formatters.moodle_course_to_BE_course import (
    moodle_course_to_BE_course,
)
from darwin.models.client_models import MoodleCourse
from darwin.models.midtier_models import (
    Account,
    BasicAssignment,
    BasicCourse as MT_BasicCourse,
    Course as MT_Course,
    CourseId,
    MoodleCourseCreate,
    Student as MT_Student,
    Ta as MT_Ta,
    Teacher as MT_Teacher,
)
from darwin.models.backend_models import (
    AccessLevel,
    AccountPermission,
    Course as BE_Course,
    AccountId,
    ResourcePermission,
    SourceType,
)
from darwin.midtier.formatters.BE_assignment_to_basic_assignment import (
    BE_assignment_to_basic_assignment,
)
from itertools import chain

course_dal = Backend.course_dal
account_dal = Backend.account_dal
student_dal = Backend.student_dal
ta_dal = Backend.ta_dal
teacher_dal = Backend.teacher_dal
assignment_dal = Backend.assignment_dal

"""
============
Accepts Midtier model, decomposes into multiple backend models, and creates them using the DAL
============
"""


class CourseService:

    @classmethod
    def get_all_basic(
        cls, account_id: Optional[AccountId] = None
    ) -> list[MT_BasicCourse]:
        if account_id is None:
            BE_courses: list[BE_Course] = course_dal.get_all()
            return [MT_BasicCourse(id=c.id, name=c.name) for c in BE_courses]
        else:
            return cls.__get_all_by_account_id(account_id)

    @staticmethod
    def __get_all_by_account_id(account_id: AccountId) -> list[MT_BasicCourse]:
        student_courses: list[BE_Course] = course_dal.get_student_courses_by_account(
            account_id
        )
        ta_courses: list[BE_Course] = course_dal.get_ta_courses_by_account(account_id)
        teacher_courses: list[BE_Course] = course_dal.get_teacher_courses_by_account(
            account_id
        )

        courses: list[MT_BasicCourse] = []
        seen_ids: set[CourseId] = set()
        for BE_course in chain(student_courses, ta_courses, teacher_courses):
            if BE_course.id in seen_ids:
                continue
            seen_ids.add(BE_course.id)
            course = MT_BasicCourse(id=BE_course.id, name=BE_course.name)
            courses.append(course)

        return courses

    @staticmethod
    def get(course_id: CourseId) -> MT_Course:
        teachers: list[MT_Teacher] = []
        tas: list[MT_Ta] = []
        students: list[MT_Student] = []
        assignments: list[BasicAssignment] = []

        BE_course = course_dal.get_by_id(course_id)
        if BE_course is None:
            raise HTTPException(404, "Course not found")
        BE_teachers = teacher_dal.get_all(course_id=course_id)
        BE_tas = ta_dal.get_all(course_id=course_id)
        BE_students = student_dal.get_all(course_id=course_id)
        BE_assignments = assignment_dal.get_all(course_id=course_id)

        account_ids = [bem.account_f for bem in chain(BE_teachers, BE_tas, BE_students)]
        account_map = {
            account.id: account for account in account_dal.get_all(account_ids)
        }

        for BE_teacher in BE_teachers:
            account = account_map[BE_teacher.account_f]
            teacher = MT_Teacher(
                id=BE_teacher.id, name=account.name, email=account.email
            )
            teachers.append(teacher)

        for BE_ta in BE_tas:
            account = account_map[BE_ta.account_f]
            ta = MT_Ta(id=BE_ta.id, name=account.name, email=account.email)
            tas.append(ta)

        for BE_student in BE_students:
            account = account_map[BE_student.account_f]
            student = MT_Student(
                id=BE_student.id, name=account.name, email=account.email
            )
            students.append(student)

        assignments = [
            BE_assignment_to_basic_assignment(BE_assignment)
            for BE_assignment in BE_assignments
        ]

        return MT_Course(
            id=BE_course.id,
            name=BE_course.name,
            teachers=teachers,
            tas=tas,
            students=students,
            assignments=assignments,
        )

    @staticmethod
    def create_moodle_course(
        account: Account, moodle_course_create: MoodleCourseCreate
    ) -> MT_Course:
        if (
            course_dal.get_by_source(
                source_type=SourceType.MOODLE, source=moodle_course_create.id
            )
            is not None
        ):
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                f"Moodle Course with id {moodle_course_create.id}",
            )

        try:
            moodle_course: MoodleCourse = MoodleClient(
                moodle_course_create.moodle_session,
            ).html_get_course(moodle_course_create.id)
        except Exception as e:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                f"Issue scraping moodle course: {e}",
            )

        # Validate creator is part of the class or admin
        if account.permission != AccountPermission.ADMIN and account.email not in map(
            lambda p: p.email, moodle_course.participants
        ):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED)

        course, accounts, students, tas, teachers = moodle_course_to_BE_course(
            moodle_course
        )

        # Create Business Models
        Backend.course_dal.create(course)
        # If account with email exists - Ignore
        Backend.account_dal.try_create_all(accounts)
        Backend.student_dal.create_all(students)
        Backend.ta_dal.create_all(tas)
        Backend.teacher_dal.create_all(teachers)

        # Create access control Models
        for student in students:
            Backend.resource_permission_dal.create(
                ResourcePermission(
                    account_id=student.account_f,
                    resource_id=course.id,
                    access_level=AccessLevel.RD,
                )
            )
        for ta in tas:
            Backend.resource_permission_dal.create(
                ResourcePermission(
                    account_id=ta.account_f,
                    resource_id=course.id,
                    access_level=AccessLevel.RD_WR,
                )
            )
        for teacher in teachers:
            Backend.resource_permission_dal.create(
                ResourcePermission(
                    account_id=teacher.account_f,
                    resource_id=course.id,
                    access_level=AccessLevel.RD_WR_DEL,
                )
            )

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

        return MT_Course(
            id=course.id,
            name=course.name,
            teachers=mt_teachers,
            tas=mt_tas,
            students=mt_students,
            assignments=[],
        )


if __name__ == "__main__":
    print(
        CourseService.get_all_basic(AccountId("8ee9f255-6515-4184-a71d-b481ad1a9a25"))
    )
    print(CourseService.get_all_basic(AccountId("kjdsfkj")))
