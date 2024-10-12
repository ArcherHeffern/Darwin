from datetime import datetime
from darwin.backend import Backend
from darwin.models.backend_models import (
    Account,
    AccountId,
    AccountPermission,
    AccountStatus,
    Assignment,
    AssignmentId,
    Blob,
    BlobId,
    BlobLocationType,
    Course,
    CourseId,
    ProjectType,
    SourceType,
    Student,
    StudentId,
    Ta,
    TaId,
    Teacher,
    TeacherId,
)


class MockData:
    COURSE_1 = Course(id=CourseId("8974845845"), name="COSI 89B", deleted=False)
    COURSE_2 = Course(id=CourseId("asdfjgk"), name="COSI 400", deleted=False)

    # Account 1
    STUDENT_ACCOUNT_1 = Account(
        id=AccountId("2938745i43u"),
        email="t@t",
        name="Timmy",
        hashed_password=None,
        status=AccountStatus.UNREGISTERED,
        permission=AccountPermission.NONE,
    )
    STUDENT_1 = Student(
        id=StudentId("helloworld"),
        account_f=STUDENT_ACCOUNT_1.id,
        course_f=COURSE_1.id,
        dropped=False,
    )

    # Account 2
    STUDENT_ACCOUNT_2 = Account(
        id=AccountId("09824jvsjfw82r"),
        email="j@j",
        name="Jimmy",
        hashed_password="fishboy",
        status=AccountStatus.REGISTERED,
        permission=AccountPermission.NONE,
    )
    STUDENT_2 = Student(
        id=StudentId("nurplehdfkjfkl"),
        account_f=STUDENT_ACCOUNT_2.id,
        course_f=COURSE_1.id,
        dropped=False,
    )

    # Account 3
    TA_ACCOUNT_1 = Account(
        id=AccountId("savjvio8549jf"),
        email="e@e",
        name="Efren",
        hashed_password=None,
        status=AccountStatus.UNREGISTERED,
        permission=AccountPermission.NONE,
    )
    STUDENT_3 = Student(
        id=StudentId("goodbyeworld"),
        account_f=TA_ACCOUNT_1.id,
        course_f=COURSE_2.id,
        dropped=False,
    )
    TA_1 = Ta(
        id=TaId("fishingisreallyfun"),
        account_f=TA_ACCOUNT_1.id,
        course_f=COURSE_1.id,
        resigned=False,
        head_ta=False,
    )

    # Account 4
    TEACHER_ACCOUNT_1 = Account(
        id=AccountId("845hwg8dskld"),
        email="l@l",
        name="Liuba",
        hashed_password=None,
        status=AccountStatus.UNREGISTERED,
        permission=AccountPermission.TEACHER,
    )
    TEACHER_1 = Teacher(
        id=TeacherId("curl;lfjd"),
        account_f=TEACHER_ACCOUNT_1.id,
        course_f=COURSE_1.id,
        resigned=False,
    )

    # Account 5
    ADMIN_ACCOUNT_1 = Account(
        id=AccountId("SUPERGODGOATED"),
        email="god@god",
        name="Adam",
        hashed_password="MassiveUziVert",
        status=AccountStatus.REGISTERED,
        permission=AccountPermission.ADMIN,
    )

    BLOB_PAXOS_SKELETON = Blob(
        id=BlobId("8725101sha"),
        location_type=BlobLocationType.DISK,
        reference="./workspace/skeletons/pa4",  # TODO: Create this!
    )

    BLOB_PAXOS_TESTS = Blob(
        id=BlobId("06782345179"),
        location_type=BlobLocationType.DISK,
        reference="./workspace/tests/pa4",  # TODO: Create this!
    )

    ASSIGNMENT_1 = Assignment(
        id=AssignmentId("HAHAGOODLUCK"),
        course_f=COURSE_1.id,
        name="PA 4: Analysis of The Part Time Parliament",
        due_date=datetime(1990, 1, 1),
        project_type=ProjectType.MAVEN,
        source_type=SourceType.DISK,
        source_reference=None,
        skeleton_f=BLOB_PAXOS_SKELETON.id,
        testfiles_f=BLOB_PAXOS_TESTS.id,
        last_downloaded=None,
        deleted=False,
    )

    @classmethod
    def create(cls):
        try:
            Backend.course_dal.create(cls.COURSE_1)
            Backend.course_dal.create(cls.COURSE_2)

            Backend.account_dal.create(cls.STUDENT_ACCOUNT_1)
            Backend.account_dal.create(cls.STUDENT_ACCOUNT_2)
            Backend.account_dal.create(cls.TA_ACCOUNT_1)
            Backend.account_dal.create(cls.TEACHER_ACCOUNT_1)
            Backend.account_dal.create(cls.ADMIN_ACCOUNT_1)

            Backend.student_dal.create(cls.STUDENT_1)
            Backend.student_dal.create(cls.STUDENT_2)
            Backend.student_dal.create(cls.STUDENT_3)

            Backend.ta_dal.create(cls.TA_1)

            Backend.teacher_dal.create(cls.TEACHER_1)

            Backend.blob_dal.create(cls.BLOB_PAXOS_SKELETON)
            Backend.blob_dal.create(cls.BLOB_PAXOS_TESTS)

            Backend.assignment_dal.create(cls.ASSIGNMENT_1)
        except:
            ...
