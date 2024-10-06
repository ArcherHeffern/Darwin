from sqlalchemy.orm import Session
from .dal_I import Dal_I
from darwin.models.backend_models import Course as M_Course, CourseId
from ..schemas import Course as S_Course


#  TODO: Dependency injection for DB Session so midtier and API don't have to think about the database. Only data

class CourseDal(Dal_I):

    @Dal_I.with_session
    def create(self, db: Session, course: M_Course):
        """Raises exception on failure"""
        db = self.session_maker()
        db_course: S_Course = S_Course(id = course.id, name = course.name, deleted = course.deleted)
        db.add(db_course)
        db.commit()
    

    @Dal_I.with_session
    def get_all(self, db: Session, show_deleted = False) -> list[M_Course]:
        if show_deleted:
            db_courses = db.query(S_Course).all()
        else:
            db_courses = db.query(S_Course).filter(S_Course.deleted == False).all()
        return [M_Course.model_validate(db_course) for db_course in db_courses]
    

    @Dal_I.with_session
    def get(self, db: Session, id: CourseId, show_deleted = False) -> list[M_Course]:
        db = self.session_maker()
        if show_deleted:
            db_course = db.query(S_Course).filter(S_Course.id == id).one()
        else:
            db_course = db.query(S_Course).filter(S_Course.id == id and S_Course.deleted == False).one()
        db.close()
        return M_Course.model_validate(db_course)
