from datetime import datetime, timedelta
from itertools import chain
from typing import Iterable, TypeAlias, Optional

from pydantic import BaseModel

from darwin.models.backend_models import (
    AccountId,
    AccountPermission,
    AccountStatus,
    AssignmentId,
    AuthTokenId,
    BlobId,
    CourseId,
    GradingMetadataId,
    NonPassingTestId,
    ProjectType,
    ResourceId,
    ResourcePermissionId,
    SourceType,
    StudentId,
    SubmissionGroupId,
    SubmissionId,
    TaId,
    TeacherId,
    TestCaseId,
    TestToRunId,
)


AssignmentSkeletonId: TypeAlias = BlobId
TestfilesId: TypeAlias = BlobId


"""
============
Account 
============
"""


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


"""
================
Assignment
================
"""


class BaseAssignment(BaseModel): ...


class BasicAssignment(BaseAssignment):
    id: AssignmentId
    name: str
    due_date: datetime


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


"""
================
AssignmentSkeleton
================
"""


class BaseAssignmentSkeleton(BaseModel): ...


class AssignmentSkeleton(BaseAssignmentSkeleton):
    id: AssignmentSkeletonId


"""
================
AuthToken
================
"""


class BaseAuthToken(BaseModel): ...


class AuthToken(BaseModel):
    auth_token: AuthTokenId
    expiration: datetime


"""
================
Course
================
"""


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

    def members(self) -> Iterable["Student|Ta|Teacher"]:
        return chain(self.students, self.tas, self.teachers)

    def has_account(self, email: str) -> bool:
        for member in self.members():
            if member.email == email:
                return True
        return False


"""
================
GradingMetadata
================
"""


class BaseGradingMetadata(BaseModel): ...


class GradingMetadata(BaseGradingMetadata): ...
"""
================
NonPassingTest
================
"""


class BaseNonPassingTest(BaseModel): ...


class NonPassingTest(BaseNonPassingTest): ...
"""
================
Student
================
"""


class BaseStudent(BaseModel):
    id: StudentId
    name: str
    email: str


class Student(BaseStudent): ...
"""
================
Ta
================
"""


class BaseTa(BaseModel):
    id: TaId
    name: str
    email: str


class Ta(BaseTa): ...
"""
================
Teacher
================
"""


class BaseTeacher(BaseModel):
    id: TeacherId
    name: str
    email: str


class TeacherCreate(BaseTeacher): ...


class Teacher(BaseTeacher): ...
"""
================
TestFiles
================
"""


class BaseTestfiles(BaseModel): ...


class TestFiles(BaseTestfiles):
    id: TestfilesId


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
