from darwin.backend.dal.dal_I import Dal_I
from darwin.models.backend_models import Ta as M_Ta, CourseId
from darwin.backend.schemas import Ta as S_Ta
from typing import Optional


class TaDal(Dal_I):
    def create(self, ta: M_Ta):
        self.create_all([ta])

    def create_all(self, tas: list[M_Ta]):
        db_tas: list[S_Ta] = []
        for ta in tas:
            db_ta = S_Ta(
                id=ta.id,
                account_f=ta.account_f,
                course_f=ta.course_f,
                resigned=ta.resigned,
                head_ta=ta.head_ta,
            )
            db_tas.append(db_ta)

        with self.db_session() as db:
            db.add_all(db_tas)
            db.commit()

    def get_all(
        self, course_id: Optional[CourseId] = None, hide_dropped: bool = True
    ) -> list[M_Ta]:
        with self.db_session() as db:
            query = db.query(S_Ta)
            if course_id:
                query = query.filter_by(course_f=course_id)
            if hide_dropped:
                query = query.filter_by(resigned=False)
            tas = query.all()
            return [M_Ta.model_validate(ta) for ta in tas]
