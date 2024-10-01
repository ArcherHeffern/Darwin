from sqlite3 import Cursor, connect, Connection
from pathlib import Path
from typing import Optional, Self

from regex import W
from models.backend_models import Account, Course, StorageException, Student
from storage.storage_I import Storage_I

# TODO: Grading config used by assignment for grading
# TODO: Notification system
# TODO: Logging system


class SQLiteStorage(Storage_I):
        
    def __init__(self, c: Connection):
        self.c = c
        self.__create_tables()

    @classmethod
    def connect(cls, database_path: Path) -> Self:
        con = connect(database_path, timeout=5)
        cur = con.cursor()
        cur.close()
        return cls(con)
    
    def disconnect(self):
        self.c.close()
    
    def __create_tables(self):
        c = self.c
        with c:
            c.execute(
                """
                --sql
                CREATE TABLE IF NOT EXISTS course (
                    id              INTEGER PRIMARY KEY,
                    name            TEXT NOT NULL,
                    deleted         BOOLEAN
                );"""
            )

            c.execute(
                """
                --sql
                CREATE TABLE IF NOT EXISTS assignment (
                    id                                      INTEGER PRIMARY KEY,
                    course_f                                INTEGER NOT NULL,
                    name                                    TEXT NOT NULL,
                    due_date                                TEXT NOT NULL,
                    project_type_f                          INTEGER NOT NULL,       -- eg. gradle
                    -- What is the source of truth data store for this assignment?
                    source_type_f                           INTEGER NOT NULL,       -- eg. moodle, disk
                    source_reference                        TEXT NOT NULL,
                    -- Where are we storing the assignment stub?
                    assignment_stub_location_type_f         INTEGER NOT NULL,       -- eg. disk, remote
                    assignment_stub_reference               TEXT NOT NULL,
                    -- Where are we storing the assignment testfiles?
                    assignment_testfiles_location_type_f    INTEGER NOT NULL,       -- eg. disk, remote
                    assignment_testfiles_reference          TEXT NOT NULL,

                    deleted                                 BOOLEAN DEFAULT (FALSE),
                    last_downloaded                         TEXT,

                    FOREIGN KEY(course_f) REFERENCES course,
                    FOREIGN KEY(project_type_f) REFERENCES project_type,
                    FOREIGN KEY(source_type_f) REFERENCES source_type,
                    FOREIGN KEY(assignment_stub_location_type_f) REFERENCES source_type
                    FOREIGN KEY(assignment_testfiles_location_type_f) REFERENCES source_type
                );"""
            )

            if not self.__table_exists('project_type'):
                c.execute(
                    """
                    --sql
                    CREATE TABLE project_type (
                        id      INTEGER PRIMARY KEY, 
                        name    TEXT NOT NULL
                    );"""
                )
                c.executemany("""
                --sql
                INSERT INTO project_type (id, name) VALUES (?, ?)
                ;
                """, ((1, 'gradle'),))
            
            if not self.__table_exists('source_type'):
                c.execute(
                    """ 
                    --sql
                    CREATE TABLE source_type (
                        id      INTEGER PRIMARY KEY,
                        name    TEXT NOT NULL
                    );"""
                )
                c.executemany(
                    """
                    --sql
                    INSERT INTO source_type (id, name) VALUES (?, ?)
                    ;""",((1, 'local_sqlite'), (2, 'moodle'),))
            
            if not self.__table_exists('blob_location_type'):
                c.execute(
                    """
                    --sql
                    CREATE TABLE blob_location_type (
                    id      INTEGER PRIMARY KEY,
                    name    TEXT NOT NULL
                    );"""
                )
                c.executemany(
                    """
                    --sql
                    INSERT INTO blob_location_type (id, name) VALUES (?, ?)
                    ;""",((1, 'disk'), (2, 'local_sqlite')))

            c.execute(
                """ 
                --sql
                CREATE TABLE IF NOT EXISTS test_to_run (
                    id              INTEGER PRIMARY KEY,
                    assignment_f    INTEGER NOT NULL,
                    name            TEXT NOT NULL,

                    FOREIGN KEY(assignment_f) REFERENCES assignment
                );"""
            )

            c.execute(
                """
                --sql
                CREATE TABLE IF NOT EXISTS user_submission (
                    id              INTEGER PRIMARY KEY,
                    student_f       INTEGER NOT NULL,
                    time            TEXT,

                    FOREIGN KEY (student_f) REFERENCES student
                );"""
            )

            c.execute(
                """
                --sql
                CREATE TABLE IF NOT EXISTS grading_metadata (
                    id              INTEGER PRIMARY KEY,
                    submission_f    INTEGER NOT NULL,
                    passing         INTEGER NOT NULL,
                    failing         INTEGER NOT NULL,
                    erroring        INTEGER NOT NULL,
                    grade           INTEGER NOT NULL,

                    FOREIGN KEY (submission_f) REFERENCES submission
                );"""
            )

            c.execute(
                """
                --sql
                CREATE TABLE IF NOT EXISTS test_case (
                    id              INTEGER PRIMARY KEY,
                    assignment_f    INTEGER NOT NULL,
                    name            TEXT,

                    FOREIGN KEY (assignment_f) REFERENCES assignment
                );"""
            )

            c.execute(
                """
                --sql
                CREATE TABLE IF NOT EXISTS non_passing_test (
                    id          INTEGER PRIMARY KEY,
                    test_case_f INTEGER NOT NULL,
                    status_f    INTEGER NOT NULL,
                    reason      TEXT NOT NULL,

                    FOREIGN KEY (test_case_f) REFERENCES test_case,
                    FOREIGN KEY (status_f) REFERENCES test_status
                ) 
                ;
                """
            )

            if not self.__table_exists('test_status'):
                c.execute(
                    """
                    --sql
                    CREATE TABLE test_status (
                        id          INTEGER PRIMARY KEY,
                        status      TEXT(20) NOT NULL
                    );"""
                )
                c.executemany(
                    """
                    --sql
                    INSERT INTO test_status (id, status) VALUES (?, ?) 
                    ;""", ((1, 'skipped'), (2, 'failing'), (3, 'erroring'))
                )

            c.execute(
                """ 
                --sql
                CREATE TABLE IF NOT EXISTS account (
                    id              INTEGER PRIMARY KEY,
                    name            TEXT(50) NOT NULL,
                    email           TEXT NOT NULL,
                    password        TEXT,
                    status_f        INTEGER NOT NULL,

                    FOREIGN KEY (status_f) REFERENCES account_status
                );"""
            )

            if not self.__table_exists('account_status'):
                c.execute(
                    """
                    --sql
                    CREATE TABLE IF NOT EXISTS account_status (
                        id      INTEGER PRIMARY KEY,
                        name    TEXT
                    );"""
                )

                c.executemany(
                    """
                    --sql
                    INSERT INTO account_status (id, name) VALUES (?, ?)
                    ;""", ((1, 'unregistered'), (2, 'registered'), (3, 'deleted')))

            c.execute(
                """
                --sql
                CREATE TABLE IF NOT EXISTS student (
                    id              INTEGER PRIMARY KEY,
                    account_f       INTEGER, 
                    course_f        INTEGER,
                    dropped         BOOLEAN,

                    FOREIGN KEY(account_f) REFERENCES account,
                    FOREIGN KEY(course_f) REFERENCES course
                );"""
            )

            c.execute(
                """
                --sql
                CREATE TABLE IF NOT EXISTS ta (
                    id              INTEGER PRIMARY KEY,
                    account_f       INTEGER, 
                    course_f        INTEGER,
                    resigned        BOOLEAN,
                    head_ta         BOOLEAN,       

                    FOREIGN KEY(account_f) REFERENCES account,
                    FOREIGN KEY(course_f) REFERENCES course
                );"""
            )

            c.execute(
                """
                --sql
                CREATE TABLE IF NOT EXISTS teacher (
                    id              INTEGER PRIMARY KEY,
                    account_f       INTEGER, 
                    course_f        INTEGER,
                    resigned        BOOLEAN,

                    FOREIGN KEY(account_f) REFERENCES account,
                    FOREIGN KEY(course_f) REFERENCES course
                );"""
            )
    
    def __table_exists(self, name: str) -> bool:
        return self.c.execute(
        """ 
        --sql
        SELECT name FROM sqlite_master WHERE type='table' AND name=?
        ;""", (name,)).fetchone() is not None

    @classmethod
    def __register_adapters(cls, c: Connection):
        ...
    
    @classmethod
    def __register_converters(cls, c: Connection):
        ...
    

    def create_course(self, course: Course) -> Course: 
        """Creates course and returns course with id filled or raises StorageException"""
        ...

    def create_student(self, student: Student) -> Student:
        """Creates student and returns course with id filled or raises StorageException"""
        if self.get_account(student.account.id) is None:
            self.create_account(student.account)
        if student.course.id is None:
            self.create_course(student.course)
        
        c = self.c

        try:
            with c:
                c.execute(
                    """
                    --sql
                    INSERT INTO student (account, course, dropped) VALUES (?, ?, ?)
                    """
                , (student.account.id, student.course.id, student.dropped))
            return student
        except Exception as e:
            raise StorageException(f'Failed to create student {student.account.name}: {e}')
    
    def get_account(self, account_id: int) -> Optional[Account]:
        c = self.c
        try: 
            with c:
                account = c.execute(
                    """
                    --sql
                    SELECT * FROM account WHERE id==?;
                    """, (str(account_id))).fetchone()
                print(account)

        except Exception as e:
            raise StorageException(f'Failed to get account of account_id {account_id}: {e}')


    def create_account(self, account: Account):
        """
        Creates account or raises StorageException
        Note: Unlike other models, we don't update the accountid since it's already filled by moodle
        """
        c = self.c
        try:
            with c:
                c.execute(
                    """
                    --sql
                    INSERT INTO account (id, name, email, password, status_f) VALUES (?, ?, ?, ?, ?);
                    """, (account.id, account.name, account.email, account.password, account.status.value))
            return account
        except Exception as e:
            raise StorageException(f'Failed to create account for {account.name}: {e}')
            
