from src.darwin.backend.dal import Dal
import src.darwin.backend.schemas as schemas
import src.darwin.models.backend_models as models
from src.darwin.backend.db_init import engine, SessionLocal
from src.darwin.backend import Backend

# Post database creation items - Post schemas and post db_init (used in dal.py)

db = Dal.create_session()

def test_create_account():
    account = schemas.Account(
        id = 0,
        email = "a@a",
        name = "Archer",
        hashed_password = "helloworld",
        status = models.AccountStatus.REGISTERED,
        permission = models.AccountPermission.ADMIN,
    )
    db.add(account)
    db.commit()
    db.refresh(account)
    x = db.query(schemas.Account).filter(schemas.Account.id == 0).first()
    if x:
        print(x.status)
        print(x.status == models.AccountStatus.REGISTERED)
        print(type(x))

    db.delete(account)
    db.commit()

def test_create_course():
    course = schemas.Course(id = 0, name = "COSI 131", deleted = False)
    Backend.course_service.create(db, course)

test_create_course()
