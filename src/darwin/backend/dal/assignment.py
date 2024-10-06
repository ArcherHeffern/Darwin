from sqlalchemy.orm import Session
from .. import schemas
from darwin.models.backend_models import Assignment, AssignmentId


class AssignmentDal:

    def get(self, db: Session, id: AssignmentId, allow_deleted = False):
        if allow_deleted:
            result = db.query(schemas.Assignment).filter(Assignment.id == id).one()
        else:
            result = db.query(schemas.Assignment).filter(Assignment.id == id and not Assignment.deleted).one()
        return Assignment.model_validate(result)
        
    
    def get_all(self, db: Session, allow_deleted: bool = False) -> list[Assignment]:
        if allow_deleted:
            results = db.query(schemas.Assignment).all()
        else:
            results = db.query(schemas.Assignment).filter(not schemas.Assignment.deleted).all()
        return [Assignment.model_validate(result) for result in results]

    

    def create(self, assignment: Assignment):
        ...
