from darwin.backend import Backend
from sqlalchemy.orm import Session
from darwin.models.backend_models import Course as M_Course, CourseId

course_dal = Backend.course_dal

"""
============
Accepts Midtier model, decomposes into multiple backend models, and creates them using the DAL
============
"""


class CourseService:
    @staticmethod
    def create(course: M_Course):
        course_dal.create(course)

    @staticmethod
    def get_all() -> list[M_Course]:
        return course_dal.get_all()

    @staticmethod
    def get(id: CourseId) -> M_Course:
        return course_dal.get(id)
