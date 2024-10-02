from sqlite3 import Connection

PROJECT_TYPES = ((1, "GRADLE"),)
SOURCE_TYPES = (
    (1, "LOCAL_SQLITE"),
    (2, "MOODLE"),
)
BLOB_LOCATION_TYPE = ((1, "DISK"), (2, "LOCAL_SQLITE"))
TEST_STATUSES = ((1, "SKIPPED"), (2, "FAILING"), (3, "ERRORING"))
ACCOUNT_STATUSES = ((1, "UNREGISTERED"), (2, "REGISTERED"), (3, "DELETED"))


class DbInit:
    def __init__(self, c: Connection):
        self.c = c

    def create_database(self):
        c = self.c
        with c:
            self.__create_account_table(c)
            self.__create_assignment_table(c)
            self.__create_course_table(c)
            self.__create_grading_metadata_table(c)
            self.__create_non_passing_test_table(c)
            self.__create_student_table(c)
            self.__create_submission_group_table(c)
            self.__create_submission_table(c)
            self.__create_ta_table(c)
            self.__create_teacher_table(c)
            self.__create_test_case_table(c)
            self.__create_test_to_run_table(c)

            # Enums
            self.__create_project_type_enum_table(c)
            self.__create_source_type_enum_table(c)
            self.__create_blob_location_type_enum_table(c)
            self.__create_test_status_enum_table(c)
            self.__create_account_status_enum_table(c)

    def __create_account_table(self, c: Connection):
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

    def __create_assignment_table(self, c):
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

                last_downloaded                         TEXT,
                deleted                                 BOOLEAN NOT NULL,

                FOREIGN KEY(course_f) REFERENCES course,
                FOREIGN KEY(project_type_f) REFERENCES project_type,
                FOREIGN KEY(source_type_f) REFERENCES source_type,
                FOREIGN KEY(assignment_stub_location_type_f) REFERENCES blob_location_type,
                FOREIGN KEY(assignment_testfiles_location_type_f) REFERENCES blob_location_type
            );"""
        )

    def __create_course_table(self, c: Connection):
        c.execute(
            """
            --sql
            CREATE TABLE IF NOT EXISTS course (
                id              INTEGER PRIMARY KEY,
                name            TEXT NOT NULL,
                deleted         BOOLEAN NOT NULL
            );"""
        )

    def __create_grading_metadata_table(self, c: Connection):
        c.execute(
            """
            --sql
            CREATE TABLE IF NOT EXISTS grading_metadata (
                id              INTEGER PRIMARY KEY,
                submission_f    INTEGER NOT NULL,
                passing         INTEGER NOT NULL,
                failing         INTEGER NOT NULL,
                erroring        INTEGER NOT NULL,
                skipped         INTEGER NOT NULL,
                grade           INTEGER NOT NULL,
                lateness        INTEGER, -- Unix time from submission
                proper_naming   BOOLEAN,

                FOREIGN KEY (submission_f) REFERENCES submission
            );"""
        )

    def __create_non_passing_test_table(self, c: Connection):
        c.execute(
            """
            --sql
            CREATE TABLE IF NOT EXISTS non_passing_test (
                id                      INTEGER PRIMARY KEY,
                submission_group_f      INTEGER NOT NULL,
                test_case_f             INTEGER NOT NULL,
                status_f                INTEGER NOT NULL,
                reason                  TEXT NOT NULL,

                FOREIGN KEY (submission_group_f) REFERENCES submission_group,
                FOREIGN KEY (test_case_f) REFERENCES test_case,
                FOREIGN KEY (status_f) REFERENCES test_status
            ) 
            ;
            """
        )

    def __create_student_table(self, c: Connection):
        c.execute(
            """
            --sql
            CREATE TABLE IF NOT EXISTS student (
                id              INTEGER PRIMARY KEY,
                account_f       INTEGER NOT NULL, 
                course_f        INTEGER NOT NULL,
                dropped         BOOLEAN NOT NULL,

                FOREIGN KEY(account_f) REFERENCES account,
                FOREIGN KEY(course_f) REFERENCES course
            );"""
        )

    def __create_submission_group_table(self, c: Connection):
        c.execute(
            """
            --sql
            CREATE TABLE IF NOT EXISTS submission_group (
                id              INTEGER PRIMARY KEY,
                student_f       INTEGER NOT NULL,
                time            TEXT NOT NULL,
                deleted         BOOLEAN NOT NULL,

                FOREIGN KEY (student_f) REFERENCES student
            );"""
        )

    def __create_submission_table(self, c: Connection):
        c.execute(
            """
            --sql
            CREATE TABLE IF NOT EXISTS submission_table (
                id                          INTEGER PRIMARY KEY,
                submission_location_type_f  INTEGER NOT NULL, 
                submission_reference        TEXT NOT NULL,
                deleted                     BOOLEAN NOT NULL,

                FOREIGN KEY (submission_location_type_f) REFERENCES blob_location_type
            );"""
        )

    def __create_ta_table(self, c: Connection):
        c.execute(
            """
            --sql
            CREATE TABLE IF NOT EXISTS ta (
                id              INTEGER PRIMARY KEY,
                account_f       INTEGER NOT NULL, 
                course_f        INTEGER NOT NULL,
                resigned        BOOLEAN NOT NULL,
                head_ta         BOOLEAN NOT NULL,

                FOREIGN KEY(account_f) REFERENCES account,
                FOREIGN KEY(course_f) REFERENCES course
            );"""
        )

    def __create_teacher_table(self, c: Connection):
        c.execute(
            """
            --sql
            CREATE TABLE IF NOT EXISTS teacher (
                id              INTEGER PRIMARY KEY,
                account_f       INTEGER NOT NULL, 
                course_f        INTEGER NOT NULL,
                resigned        BOOLEAN NOT NULL,

                FOREIGN KEY(account_f) REFERENCES account,
                FOREIGN KEY(course_f) REFERENCES course
            );"""
        )

    def __create_test_case_table(self, c: Connection):
        c.execute(
            """
            --sql
            CREATE TABLE IF NOT EXISTS test_case (
                id              INTEGER PRIMARY KEY,
                assignment_f    INTEGER NOT NULL,
                name            TEXT NOT NULL,

                FOREIGN KEY (assignment_f) REFERENCES assignment
            );"""
        )

    def __create_test_to_run_table(self, c: Connection):
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

    ###########################
    # ======== ENUMS ======== #
    ###########################

    def __create_project_type_enum_table(self, c: Connection):
        c.execute(
            """
            --sql
            CREATE TABLE IF NOT EXISTS project_type (
                id      INTEGER PRIMARY KEY, 
                name    TEXT NOT NULL UNIQUE
            );"""
        )
        c.executemany(
            """
        --sql
        INSERT OR IGNORE INTO project_type (id, name) VALUES (?, ?)
        ;
        """,
            PROJECT_TYPES,
        )

    def __create_source_type_enum_table(self, c: Connection):
        c.execute(
            """ 
            --sql
            CREATE TABLE IF NOT EXISTS source_type (
                id      INTEGER PRIMARY KEY,
                name    TEXT NOT NULL UNIQUE
            );"""
        )
        c.executemany(
            """
            --sql
            INSERT OR IGNORE INTO source_type (id, name) VALUES (?, ?)
            ;""",
            SOURCE_TYPES,
        )

    def __create_blob_location_type_enum_table(self, c: Connection):
        c.execute(
            """
            --sql
            CREATE TABLE IF NOT EXISTS blob_location_type (
            id      INTEGER PRIMARY KEY,
            name    TEXT NOT NULL UNIQUE
            );"""
        )
        c.executemany(
            """
            --sql
            INSERT OR IGNORE INTO blob_location_type (id, name) VALUES (?, ?)
            ;""",
            BLOB_LOCATION_TYPE,
        )

    def __create_test_status_enum_table(self, c: Connection):
        c.execute(
            """
            --sql
            CREATE TABLE IF NOT EXISTS test_status (
                id          INTEGER PRIMARY KEY,
                status      TEXT NOT NULL UNIQUE
            );"""
        )
        c.executemany(
            """
            --sql
            INSERT OR IGNORE INTO test_status (id, status) VALUES (?, ?) 
            ;""",
            TEST_STATUSES,
        )

    def __create_account_status_enum_table(self, c: Connection):
        c.execute(
            """
            --sql
            CREATE TABLE IF NOT EXISTS account_status (
                id      INTEGER PRIMARY KEY,
                name    TEXT NOT NULL UNIQUE 
            );"""
        )

        c.executemany(
            """
            --sql
            INSERT OR IGNORE INTO account_status (id, name) VALUES (?, ?)
            ;""",
            ACCOUNT_STATUSES,
        )
