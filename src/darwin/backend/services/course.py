from ..dal import Dal
from sqlalchemy.orm import Session
from darwin.models.backend_models import Course as M_Course, CourseId

course_dal = Dal.course_dal

"""
============
Accepts Midtier model, decomposes into multiple backend models, and creates them using the DAL
============
"""
class CourseService:
    def create(self, course: M_Course):
        course_dal.create(course)

    def get_all(self) -> list[M_Course]:
        return course_dal.get_all()
    
    def get(self, id: CourseId) -> M_Course:
        return course_dal.get(id)