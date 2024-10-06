from pydantic import BaseModel
from typing import NewType
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional

"""
============
IDs
============
"""
CourseId = NewType("CourseId", int)
AssignmentId = NewType("AssignmentId", int)
TestToRunId = NewType("TestToRunId", int)
AccountId = NewType("AccountId", int)
TeacherId = NewType("TeacherId", int)
TaId = NewType("TaId", int)
StudentId = NewType("StudentId", int)
SubmissionId = NewType("SubmissionId", int)
GradingMetadataId = NewType("GradingMetadataId", int)
NonPassingTestId = NewType("NonPassingTestId", int)
TestCaseId = NewType("TestCaseId", int)
SubmissionGroupId = NewType("SubmissionGroupId", int)


"""
============
Account 
============
"""
class Account(BaseModel):
    id: AccountId
    email: str
    name: str  # Capitalized
    hashed_password: Optional["str"]  # Null if account is inactive
    status: "AccountStatus"
    permission: 'AccountPermission'

    class Config:
        from_attributes = True


"""
============
Assignment 
============
"""
class Assignment(BaseModel):
    id: AssignmentId
    course_f: CourseId
    name: str
    due_date: datetime
    project_type_f: "ProjectType"
    source_type: "SourceType"
    source_reference: str
    assignment_stub_location_type_f: "BlobLocationType"
    assignment_stub_reference: str
    assignment_testfiles_location_type_f: "BlobLocationType"
    assignment_testfiles_reference: str
    last_downloaded: Optional[datetime]
    deleted: bool

    class Config:
        from_attributes = True

"""
============
Course
============
"""
class Course(BaseModel):
    id: CourseId
    name: str
    deleted: bool

    class Config:
        from_attributes = True


"""
============
GradingMetadata
============
"""
class GradingMetadata(BaseModel):
    id: GradingMetadataId
    submission_f: SubmissionId
    passing: int
    failing: int
    erroring: int
    skipped: int
    grade: int
    lateness: Optional[timedelta]  # Will be converted to Unix time
    proper_naming: bool

    class Config:
        from_attributes = True


class NonPassingTest(BaseModel):
    id: NonPassingTestId
    submission_group_f: SubmissionGroupId
    test_case_f: TestCaseId
    status_f: "TestStatus"
    reason: str

    class Config:
        from_attributes = True


class Student(BaseModel):
    id: StudentId
    account_f: AccountId
    course_f: CourseId
    dropped: bool

    class Config:
        from_attributes = True


class SubmissionGroup(BaseModel):
    id: SubmissionGroupId
    student: StudentId
    time: datetime
    deleted: bool

    class Config:
        from_attributes = True


class Submission(BaseModel):
    id: SubmissionId
    submission_location_type_f: "BlobLocationType"
    submission_reference: str
    deleted: bool

    class Config:
        from_attributes = True


class Ta(BaseModel):
    id: TaId
    account: AccountId
    course_f: CourseId
    resigned: bool
    head_ta: bool

    class Config:
        from_attributes = True


class Teacher(BaseModel):
    id: TeacherId
    account_f: AccountId
    course_f: CourseId
    resigned: bool

    class Config:
        from_attributes = True


class TestCase(BaseModel):
    id: TestCaseId
    assignment_f: AssignmentId
    name: str

    class Config:
        from_attributes = True


class TestToRun(BaseModel):
    id: TestToRunId
    assignment_f: AssignmentId
    name: str

    class Config:
        from_attributes = True


###########################
# ======== ENUMS ======== #
###########################


class ProjectType(Enum):
    MAVEN = 0


class SourceType(Enum):
    MOODLE = 0
    DISK = 1


class BlobLocationType(Enum):
    DISK = 0
    LOCAL_SQLITE = 1


class TestStatus(Enum):
    SKIPPED = 1
    FAILING = 2
    ERRORING = 3


class AccountStatus(Enum):
    UNREGISTERED = 1
    REGISTERED = 2
    DELETED = 3
    REQUESTED = 4
    DENIED = 5

class AccountPermission(Enum):
    NONE = 1
    TEACHER = 2
    ADMIN = 3

# Exceptions
class StorageException(RuntimeError): ...


class BadConfigException(RuntimeError): ...


class ProjectExecutionException(RuntimeError): ...


class ProjectValidationException(RuntimeError): ...
