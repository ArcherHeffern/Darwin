from darwin.models.backend_models import (
    AccountPermission,
    AccountStatus,
    Course as BE_Course,
    SourceType,
    Student as BE_Student,
    StudentId as BE_StudentId,
    Account as BE_Account,
    AccountId as BE_AccountId,
    CourseId as BE_CourseId,
    Teacher as BE_Teacher,
    TeacherId as BE_TeacherId,
    Ta as BE_Ta,
    TaId as BE_TaId,
)
from uuid import uuid4
from darwin.models.client_models import MoodleCourse, MoodleCourseParticipantRole


def moodle_course_to_BE_course(
    moodle_course: MoodleCourse,
) -> tuple[
    BE_Course, list[BE_Account], list[BE_Student], list[BE_Ta], list[BE_Teacher]
]:
    course_id = BE_CourseId(str(uuid4()))
    course = BE_Course(
        id=course_id,
        name=moodle_course.name,
        deleted=False,
        source_type=SourceType.MOODLE,
        source=moodle_course.id,
    )
    accounts: list[BE_Account] = []
    students: list[BE_Student] = []
    tas: list[BE_Ta] = []
    teachers: list[BE_Teacher] = []

    for participant in moodle_course.participants:
        account_id = BE_AccountId(str(uuid4()))
        account: BE_Account = BE_Account(
            id=account_id,
            email=participant.email,
            name=participant.name,
            hashed_password=None,
            status=AccountStatus.UNREGISTERED,
            permission=AccountPermission.MEMBER,
        )
        match participant.role:
            case MoodleCourseParticipantRole.STUDENT:
                student_id = BE_StudentId(str(uuid4()))
                students.append(
                    BE_Student(
                        id=student_id,
                        account_f=account_id,
                        course_f=course_id,
                        dropped=False,
                    )
                )
            case MoodleCourseParticipantRole.INSTRUCTOR:
                account.permission = AccountPermission.TEACHER
                teacher_id = BE_TeacherId(str(uuid4()))
                teachers.append(
                    BE_Teacher(
                        id=teacher_id,
                        account_f=account_id,
                        course_f=course_id,
                        resigned=False,
                    )
                )
            case MoodleCourseParticipantRole.NONE:
                student_id = BE_TaId(str(uuid4()))
                tas.append(
                    BE_Ta(
                        id=student_id,
                        account_f=account_id,
                        course_f=course_id,
                        resigned=False,
                        head_ta=False,
                    )
                )
        accounts.append(account)

    return course, accounts, students, tas, teachers
