from sqlalchemy.orm.session import Session
from .dal_I import Dal_I
from darwin.models.backend_models import Course as M_Course, CourseId
from ..schemas import Course as S_Course


class CourseDal(Dal_I):

    def create(self, course: M_Course):
        with self.db_session() as db:
            db_course: S_Course = S_Course(id = course.id, name = course.name, deleted = course.deleted)
            db.add(db_course)
            db.commit()
    

    def get_all(self, show_deleted = False) -> list[M_Course]:
        with self.db_session() as db:
            if show_deleted:
                db_courses = db.query(S_Course).all()
            else:
                db_courses = db.query(S_Course).filter(S_Course.deleted == False).all()
            return [M_Course.model_validate(db_course) for db_course in db_courses]
    

    def get(self, id: CourseId, show_deleted = False) -> M_Course:
        with self.db_session() as db:
            if show_deleted:
                db_course = db.query(S_Course).filter(S_Course.id == id).one()
            else:
                db_course = db.query(S_Course).filter(S_Course.id == id and S_Course.deleted == False).one()
            db.close()
            return M_Course.model_validate(db_course)
