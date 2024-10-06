from sqlalchemy.orm import Session

from darwin.backend.dal.dal_I import Dal_I
from .. import schemas
from darwin.models.backend_models import Assignment, AssignmentId


class AssignmentDal(Dal_I):

    def get(self, id: AssignmentId, allow_deleted=False):
        with self.db_session() as db:
            if allow_deleted:
                result = db.query(schemas.Assignment).filter(Assignment.id == id).one()
            else:
                result = (
                    db.query(schemas.Assignment)
                    .filter(Assignment.id == id and not Assignment.deleted)
                    .one()
                )
        return Assignment.model_validate(result)

    def get_all(self, allow_deleted: bool = False) -> list[Assignment]:
        with self.db_session() as db:
            if allow_deleted:
                results = db.query(schemas.Assignment).all()
            else:
                results = (
                    db.query(schemas.Assignment)
                    .filter(schemas.Assignment.deleted == False)
                    .all()
                )
            return [Assignment.model_validate(result) for result in results]

    def create(self, assignment: Assignment): ...
