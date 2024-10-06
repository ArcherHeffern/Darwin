from abc import ABC
from contextlib import contextmanager
from typing import Generator
from typing_extensions import deprecated
from sqlalchemy.orm.session import Session, sessionmaker


class Dal_I(ABC):
    def __init__(self, session_maker: sessionmaker[Session]):
        self.__session_maker = session_maker

    @contextmanager
    def db_session(self) -> Generator[Session, None, None]:
        """
        context manager to provide database session

        Provides type hinting for functions using a db session unlike the predecessor `with_session`

        Usage:
        def get(self, *args, **kwargs):
            with self.db_session() as db:
                ...

        """
        db = self.__session_maker()
        try:
            yield db
            db.commit()
        except:
            db.rollback()
            raise
        finally:
            db.close()

    @staticmethod
    @deprecated("Use get_session instead for better type safety")
    def with_session(method):
        """
        Decorator to provide database session

        Warning Deprecated! Use get_session instead

        Usage:
        @Dal_I.with_session
        def get(self, db: sqlalchemy.orm.session.Session, *args, **kwargs):
            ...
        """

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
