# type: ignore
from darwin.models.backend_models import (
    AccessLevel,
    AccountId,
    AccountCreateTokenId,
    AccountPermission,
    AccountStatus,
    AssignmentId,
    AuthTokenId,
    BlobId,
    BlobLocationType,
    CourseId,
    GradingMetadataId,
    NonPassingTestId,
    ProjectType,
    ResourceId,
    SourceType,
    StudentId,
    SubmissionGroupId,
    SubmissionId,
    TaId,
    TeacherId,
    TestCaseId,
    TestStatus,
    TestToRunId,
)
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
)
from datetime import datetime
from sqlalchemy.orm import relationship
from typing import Optional


from .db_init import Base


class Account(Base):
    __tablename__ = "account"

    id: AccountId = Column(String, primary_key=True)
    email: str = Column(String, unique=True, index=True, nullable=False)
    name: str = Column(String, nullable=False)
    hashed_password: str | None = Column(String, nullable=True)
    status: AccountStatus = Column(Enum(AccountStatus), nullable=False)
    permission: AccountPermission = Column(Enum(AccountPermission), nullable=False)


class AccountCreateToken(Base):
    __tablename__ = "account_create_token"

    id: AccountCreateTokenId = Column(String, primary_key=True)
    email: str = Column(String, nullable=False)
    expiration: datetime = Column(DateTime, nullable=False)


class Assignment(Base):
    __tablename__ = "assignment"

    id: AssignmentId = Column(String, primary_key=True)
    course_f: CourseId = Column(String, ForeignKey("course.id"), nullable=False)
    name: str = Column(Text, nullable=False)
    due_date: datetime = Column(DateTime, nullable=False)
    project_type: ProjectType = Column(Enum(ProjectType), nullable=False)
    source_type: SourceType = Column(Enum(SourceType), nullable=False)
    source_reference: str = Column(Text, nullable=True)
    skeleton_f: Optional[BlobId] = Column(String, ForeignKey("blob.id"), nullable=True)
    testfiles_f: BlobId = Column(String, ForeignKey("blob.id"), nullable=False)
    last_downloaded: datetime = Column(DateTime, nullable=True)
    deleted: bool = Column(Boolean, nullable=False, default=False)

    course = relationship("Course")
    skeleton = relationship("Blob", primaryjoin="Assignment.skeleton_f == Blob.id")
    testfiles = relationship("Blob", primaryjoin="Assignment.testfiles_f == Blob.id")


class AuthToken(Base):
    __tablename__ = "auth_token"

    token: AuthTokenId = Column(String, primary_key=True)
    account_f: AccountId = Column(String, ForeignKey("account.id"), nullable=False)
    expiration: datetime = Column(DateTime, nullable=False)
    revoked: bool = Column(Boolean, nullable=False)

    account = relationship("Account")


class Blob(Base):
    __tablename__ = "blob"

    id: BlobId = Column(String, primary_key=True)
    location_type: BlobLocationType = Column(Enum(BlobLocationType), nullable=False)
    reference: str = Column(String, nullable=False)


class Course(Base):
    __tablename__ = "course"

    id: CourseId = Column(String, primary_key=True)
    name: str = Column(Text, nullable=False)
    deleted: bool = Column(Boolean, nullable=False)
    source_type: SourceType = Column(Enum(SourceType), nullable=False)
    source: Optional[str] = Column(String, nullable=True)


class GradingMetadata(Base):
    __tablename__ = "grading_metadata"

    id: GradingMetadataId = Column(String, primary_key=True)
    submission_f: SubmissionId = Column(
        String, ForeignKey("submission.id"), nullable=False
    )
    passing: int = Column(Integer, nullable=False, default=0)
    failing: int = Column(Integer, nullable=False, default=0)
    erroring: int = Column(Integer, nullable=False, default=0)
    skipped: int = Column(Integer, nullable=False, default=0)
    grade: int = Column(Integer, nullable=False, default=0)
    lateness: int = Column(Integer, nullable=True)
    proper_naming: bool = Column(Boolean, nullable=True)

    submission = relationship("Submission")


class NonPassingTest(Base):
    __tablename__ = "non_passing_test"

    id: NonPassingTestId = Column(String, primary_key=True)
    submission_group_f: SubmissionGroupId = Column(
        String, ForeignKey("submission_group.id"), nullable=False
    )
    test_case_f: TestCaseId = Column(String, ForeignKey("test_case.id"), nullable=False)
    status_f: TestStatus = Column(Enum(TestStatus), nullable=False)
    reason: str = Column(Text, nullable=False)

    submission_group = relationship("SubmissionGroup")
    test_case = relationship("TestCase")


class ResourcePermission(Base):
    __tablename__ = "resource_permission"

    account_id: AccountId = Column(
        String, ForeignKey("account.id"), primary_key=True, nullable=False
    )
    resource_id: ResourceId = Column(String, primary_key=True)
    access_level: AccessLevel = Column(Enum(AccessLevel), nullable=False)


class Student(Base):
    __tablename__ = "student"

    id: StudentId = Column(String, primary_key=True)
    account_f: AccountId = Column(String, ForeignKey("account.id"), nullable=False)
    course_f: CourseId = Column(String, ForeignKey("course.id"), nullable=False)
    dropped: bool = Column(Boolean, nullable=False)

    account = relationship("Account")
    course = relationship("Course")


class SubmissionGroup(Base):
    __tablename__ = "submission_group"

    id: SubmissionGroupId = Column(String, primary_key=True)
    student_f: StudentId = Column(String, ForeignKey("student.id"), nullable=False)
    time: str = Column(Text, nullable=False)
    deleted: bool = Column(Boolean, nullable=False)

    student = relationship("Student")


class Submission(Base):
    __tablename__ = "submission"

    id: SubmissionId = Column(String, primary_key=True)
    submission_location_type: BlobLocationType = Column(
        Enum(BlobLocationType), nullable=False
    )
    submission_reference: str = Column(Text, nullable=False)
    deleted: bool = Column(Boolean, nullable=False)


class Ta(Base):
    __tablename__ = "ta"

    id: TaId = Column(String, primary_key=True)
    account_f: AccountId = Column(String, ForeignKey("account.id"), nullable=False)
    course_f: CourseId = Column(String, ForeignKey("course.id"), nullable=False)
    resigned: bool = Column(Boolean, nullable=False)
    head_ta: bool = Column(Boolean, nullable=False)

    account = relationship("Account")
    course = relationship("Course")


class Teacher(Base):
    __tablename__ = "teacher"

    id: TeacherId = Column(String, primary_key=True)
    account_f: AccountId = Column(String, ForeignKey("account.id"), nullable=False)
    course_f: CourseId = Column(String, ForeignKey("course.id"), nullable=False)
    resigned: bool = Column(Boolean, nullable=False)

    account = relationship("Account")
    course = relationship("Course")


class TestCase(Base):
    __tablename__ = "test_case"

    id: TestCaseId = Column(String, primary_key=True)
    assignment_f: AssignmentId = Column(
        String, ForeignKey("assignment.id"), nullable=False
    )
    name: str = Column(Text, nullable=False)

    assignment = relationship("Assignment")


class TestToRun(Base):
    __tablename__ = "test_to_run"

    id: TestToRunId = Column(String, primary_key=True)
    assignment_f: AssignmentId = Column(
        String, ForeignKey("assignment.id"), nullable=False
    )
    name: str = Column(Text, nullable=False)

    assignment = relationship("Assignment")
