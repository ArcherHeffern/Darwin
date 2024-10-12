from typing import Optional
from fastapi import HTTPException
from darwin.backend import Backend
from darwin.models.midtier_models import (
    BasicAssignment,
    BasicCourse as MT_BasicCourse,
    Course as MT_Course,
    CourseId,
    Student,
    Ta,
    Teacher,
)
from darwin.models.backend_models import Course as BE_Course, AccountId
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
    # @staticmethod
    # def create(course: M_Course) -> MT_Course:
    #     course_dal.create(course)

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
        teachers: list[Teacher] = []
        tas: list[Ta] = []
        students: list[Student] = []
        assignments: list[BasicAssignment] = []

        BE_course = course_dal.get(course_id)
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
            teacher = Teacher(id=BE_teacher.id, name=account.name, email=account.email)
            teachers.append(teacher)

        for BE_ta in BE_tas:
            account = account_map[BE_ta.account_f]
            ta = Ta(id=BE_ta.id, name=account.name, email=account.email)
            tas.append(ta)

        for BE_student in BE_students:
            account = account_map[BE_student.account_f]
            student = Student(id=BE_student.id, name=account.name, email=account.email)
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


if __name__ == "__main__":
    print(
        CourseService.get_all_basic(AccountId("8ee9f255-6515-4184-a71d-b481ad1a9a25"))
    )
    print(CourseService.get_all_basic(AccountId("kjdsfkj")))
