from abc import ABC
from sqlalchemy.orm import Session, sessionmaker


class Dal_I(ABC):
    def __init__(self, session_maker: sessionmaker[Session]):
        self.session_maker = session_maker

    def with_session(method):
        def wrapper(self, *args, **kwargs):
            session = self.session_maker()
            try:
                result = method(self, session, *args, **kwargs)
                session.commit()
                return result
            except:
                session.rollback()
                raise
            finally:
                session.close()
        return wrapper