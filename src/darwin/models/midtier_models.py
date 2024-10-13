from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import NewType, Optional
from darwin.models.backend_models import (
    AccountId,
    AccountPermission,
    AccountStatus,
    AssignmentId,
    TaId,
    BlobId,
    CourseId,
    StudentId,
    TeacherId,
    TestCaseId,
    TestToRunId,
    AuthTokenId,
    SubmissionId,
    NonPassingTestId,
    GradingMetadataId,
    SubmissionGroupId,
    ProjectType,
    SourceType,
)


# ================
# Course
# ================
class BaseAccount(BaseModel): ...


class AccountCreateP1(BaseAccount):
    email: str

class AccountCreateP1Response(BaseModel):
    ttl: timedelta

class AccountCreateP2(BaseAccount):
    name: str
    password: str


class Account(BaseAccount):
    id: AccountId
    email: str
    name: str  # Capitalized
    status: AccountStatus
    permission: AccountPermission


# ================
# Course
# ================
class BaseCourse(BaseModel): ...


class MoodleCourseCreate(BaseCourse):
    id: CourseId
    moodle_session: str


class NormalCourseCreate(BaseCourse):
    id: Optional[CourseId]
    name: str


class BasicCourse(BaseCourse):
    id: CourseId
    name: str


class Course(BaseCourse):
    id: CourseId
    name: str
    teachers: list["Teacher"]
    tas: list["Ta"]
    students: list["Student"]
    assignments: list["BasicAssignment"]


# class CourseGetExtended(BaseCourse):
#     teachers: list["TeacherGet"]
#     students: list["StudentGet"]
#     tas: list["TaGet"]
#     assignments: list["AssignmentGet"]


# ================
# Teacher
# ================
class BaseTeacher(BaseModel):
    id: TeacherId
    name: str
    email: str


class TeacherCreate(BaseTeacher): ...


class Teacher(BaseTeacher): ...


# ================
# TA
# ================
class BaseTa(BaseModel):
    id: TaId
    name: str
    email: str


class Ta(BaseTa): ...


# ================
# Student
# ================
class BaseStudent(BaseModel):
    id: StudentId
    name: str
    email: str


class Student(BaseStudent): ...


# ================
# Assignment
# ================
class BaseAssignment(BaseModel): ...


class BasicAssignment(BaseAssignment):
    id: AssignmentId
    name: str
    due_date: datetime


class Assignment(BaseAssignment):
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


class CreateAssignment(BaseAssignment):
    id: Optional[AssignmentId]
    course_f: CourseId
    name: str
    due_date: datetime
    project_type: "ProjectType"
    source_type: "SourceType"
    source_reference: Optional[str]
    skeleton_f: Optional[BlobId]
    testfiles_f: BlobId


# @dataclass
# class Account:
#     id: int  # Student id - Not nullable because this is known by moodle
#     name: str  # Capitalized
#     email: str
#     password: Optional["str"]  # Null if account is inactive
#     status: "AccountState"


# class AccountState(Enum):
#     inactive = 0
#     active = 1
#     deleted = 2


# @dataclass
# class TestResult:
#     passing_tests: list["TestCase"]
#     erroring_tests: list["TestCase"]
#     skipped_tests: list["TestCase"]
#     failing_tests: list["TestCase"]


# @dataclass
# class TestCase:
#     name: str
#     classname: str
#     time: str
#     failure: Optional[str]
#     error: Optional[str]


# @dataclass
# class FileSubmission:
#     download_url: str
#     date: datetime
#     file: Optional[Path] = None


# @dataclass
# class GradingData:
#     # Assume positive unless proven otherwise
#     late: Optional[timedelta] = None
#     proper_naming: bool = True
#     grade: Optional[int] = None

#     @property
#     def graded(self):
#         return self.grade is not None


# class FileSubmissionGroup:
#     def __init__(
#         self,
#         file_submissions: list[FileSubmission],
#         assignment_config: Assignment,
#     ):
#         assert len(file_submissions) > 0

#         self.file_submissions = file_submissions

#         self.assignment_config = assignment_config

#         # All submissions in FileSubmissionGroup must have the same date
#         self.date: datetime = file_submissions[0].date

#         self.lateness = None
#         if self.date > assignment_config.due_date:
#             self.lateness = self.date - assignment_config.due_date
#         self.grading_data: GradingData = GradingData(late=self.lateness)
#         self.__filename: Optional[str] = None

#     def __str__(self) -> str:
#         return str(self.file_submissions)

#     def __repr__(self) -> str:
#         return str(self.file_submissions)

#     @property
#     def late(self) -> bool:
#         return self.lateness is not None

#     def get_filename(self, student: "Student") -> str:
#         if self.__filename:
#             return self.__filename
#         filename: str = (
#             str(student.id)
#             + "_"
#             + "".join(student.account.name.split())
#             + "_"
#             + str(self.assignment_config.name)
#         )
#         self.__filename = filename
#         return filename


# # Exceptions
# class StorageException(RuntimeError): ...


# class BadConfigException(RuntimeError): ...


# class ProjectExecutionException(RuntimeError): ...


# class ProjectValidationException(RuntimeError): ...
