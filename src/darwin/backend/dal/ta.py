from darwin.backend.dal.dal_I import Dal_I
from darwin.models.backend_models import Ta as M_Ta
from darwin.backend.schemas import Ta as S_Ta


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
