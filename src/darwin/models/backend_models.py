from dataclasses import dataclass
from typing import NewType
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional

# This is a lightweight approach to backend models
# These models almost exactly reflect how data is stored in our database. The only exceptions are Enums, which will be resolved.

# IDs
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


@dataclass
class Account:
    id: AccountId
    email: str
    name: str  # Capitalized
    password: Optional["str"]  # Null if account is inactive
    status: "AccountStatus"
    permission: 'AccountPermission'


@dataclass
class Assignment:
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


@dataclass
class Course:
    id: CourseId
    name: str
    deleted: bool


@dataclass
class GradingMetadata:
    id: GradingMetadataId
    submission_f: SubmissionId
    passing: int
    failing: int
    erroring: int
    skipped: int
    grade: int
    lateness: Optional[timedelta]  # Will be converted to Unix time
    proper_naming: bool


@dataclass
class NonPassingTest:
    id: NonPassingTestId
    submission_group_f: SubmissionGroupId
    test_case_f: TestCaseId
    status_f: "TestStatus"
    reason: str


@dataclass
class Student:
    id: StudentId
    account_f: AccountId
    course_f: CourseId
    dropped: bool


@dataclass
class SubmissionGroup:
    id: SubmissionGroupId
    student: StudentId
    time: datetime
    deleted: bool


@dataclass
class Submission:
    id: SubmissionId
    submission_location_type_f: "BlobLocationType"
    submission_reference: str
    deleted: bool


@dataclass
class Ta:
    id: TaId
    account: AccountId
    course_f: CourseId
    resigned: bool
    head_ta: bool


@dataclass
class Teacher:
    id: TeacherId
    account_f: AccountId
    course_f: CourseId
    resigned: bool


@dataclass
class TestCase:
    id: TestCaseId
    assignment_f: AssignmentId
    name: str


@dataclass
class TestToRun:
    id: TestToRunId
    assignment_f: AssignmentId
    name: str


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
