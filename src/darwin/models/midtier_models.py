from re import I
from pydantic import BaseModel
from datetime import datetime
from typing import NewType, Optional
from darwin.models.backend_models import (
    AccountId,
    TaId,
    CourseId,
    StudentId,
    TeacherId,
    TestCaseId,
    TestToRunId,
    AssignmentId,
    SubmissionId,
    NonPassingTestId,
    GradingMetadataId,
    SubmissionGroupId,
)


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
class BaseAssignment(BaseModel):
    id: AssignmentId


class BasicAssignment(BaseAssignment):
    name: str
    due_date: datetime


# class Assignment(BaseModel):
#     id: Optional[int]
#     name: str
#     due_date: datetime
#     source: Literal["moodle"]
#     project_type: Literal["maven"]
#     tests_to_run: list[str]

#     metadata: "AssignmentMetadata"


# class AssignmentMetadata:
#     last_downloaded: Optional[datetime]


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
