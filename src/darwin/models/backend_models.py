from datetime import datetime, timedelta
from enum import Enum
from typing import NewType, Optional, TypeAlias

from pydantic import BaseModel

"""
============
IDs
============
"""
AccountId = NewType("AccountId", str)
AccountCreateTokenId = NewType("AccountCreateTokenId", str)
AssignmentId = NewType("AssignmentId", str)
AuthTokenId = NewType("AuthTokenId", str)
BlobId = NewType("BlobId", str)
CourseId = NewType("CourseId", str)
GradingMetadataId = NewType("GradingMetadataId", str)
NonPassingTestId = NewType("NonPassingTestId", str)
ResourcePermissionId = NewType("ResourcePermissionId", str)
StudentId = NewType("StudentId", str)
SubmissionGroupId = NewType("SubmissionGroupId", str)
SubmissionId = NewType("SubmissionId", str)
TaId = NewType("TaId", str)
TeacherId = NewType("TeacherId", str)
TestCaseId = NewType("TestCaseId", str)
TestToRunId = NewType("TestToRunId", str)

ResourceId: TypeAlias = (
    AssignmentId | BlobId | CourseId | GradingMetadataId | NonPassingTestId | StudentId
)


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
    permission: "AccountPermission"

    class Config:
        from_attributes = True


"""
============
AccountCreateToken 
============
"""


class AccountCreateToken(BaseModel):
    id: AccountCreateTokenId
    email: str
    expiration: datetime

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
    project_type: "ProjectType"
    source_type: "SourceType"
    source_reference: Optional[str]
    skeleton_f: Optional[BlobId]
    testfiles_f: BlobId
    last_downloaded: Optional[datetime]
    deleted: bool

    class Config:
        from_attributes = True


"""
============
AuthToken
============
"""


class AuthToken(BaseModel):
    token: AuthTokenId
    account_f: AccountId
    expiration: datetime
    revoked: bool

    def expired(self) -> bool:
        return self.expiration < datetime.now()

    class Config:
        from_attributes = True


"""
============
Blob
============
"""


class Blob(BaseModel):
    id: BlobId
    location_type: "BlobLocationType"
    reference: str

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
    source_type: "SourceType"
    source: Optional[str] = None

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


"""
============
NonPassingTest
============
"""


class NonPassingTest(BaseModel):
    id: NonPassingTestId
    submission_group_f: SubmissionGroupId
    test_case_f: TestCaseId
    status_f: "TestStatus"
    reason: str

    class Config:
        from_attributes = True


"""
============
ResourcePermission
============
"""


class ResourcePermission(BaseModel):
    account_id: AccountId
    resource_id: ResourceId
    access_level: "AccessLevel"

    class Config:
        from_attributes = True


"""
============
Student
============
"""


class Student(BaseModel):
    id: StudentId
    account_f: AccountId
    course_f: CourseId
    dropped: bool

    class Config:
        from_attributes = True


"""
============
SubmissionGroup
============
"""


class SubmissionGroup(BaseModel):
    id: SubmissionGroupId
    student: StudentId
    time: datetime
    deleted: bool

    class Config:
        from_attributes = True


"""
============
Submission
============
"""


class Submission(BaseModel):
    id: SubmissionId
    submission_location_type_f: "BlobLocationType"
    submission_reference: str
    deleted: bool

    class Config:
        from_attributes = True


"""
============
Ta
============
"""


class Ta(BaseModel):
    id: TaId
    account_f: AccountId
    course_f: CourseId
    resigned: bool
    head_ta: bool

    class Config:
        from_attributes = True


"""
============
Teacher
============
"""


class Teacher(BaseModel):
    id: TeacherId
    account_f: AccountId
    course_f: CourseId
    resigned: bool

    class Config:
        from_attributes = True


"""
============
TestCase
============
"""


class TestCase(BaseModel):
    id: TestCaseId
    assignment_f: AssignmentId
    name: str

    class Config:
        from_attributes = True


"""
============
TestToRun
============
"""


class TestToRun(BaseModel):
    id: TestToRunId
    assignment_f: AssignmentId
    name: str

    class Config:
        from_attributes = True


###########################
# ======== ENUMS ======== #
###########################


class AccessLevel(Enum):
    NONE = 0
    RD = 1
    RD_WR = 3
    RD_WR_DEL = 4


class AccountPermission(Enum):
    MEMBER = 1
    TA = 2
    TEACHER = 3
    ADMIN = 4


class AccountStatus(Enum):
    UNREGISTERED = 1
    REGISTERED = 2
    DELETED = 3


class BlobLocationType(Enum):
    DISK = 0
    LOCAL_SQLITE = 1


class ProjectType(Enum):
    MAVEN = 0


class SourceType(Enum):
    MOODLE = 0
    DISK = 1


class TestStatus(Enum):
    SKIPPED = 1
    FAILING = 2
    ERRORING = 3


# Exceptions
class StorageException(RuntimeError): ...


class BadConfigException(RuntimeError): ...


class ProjectExecutionException(RuntimeError): ...


class ProjectValidationException(RuntimeError): ...
