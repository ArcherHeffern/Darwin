from fastapi import APIRouter, HTTPException, status
from darwin.midtier.services.course import CourseService
from darwin.models.backend_models import AccountPermission
from darwin.models.midtier_models import (
    MoodleCourseCreate,
    Course,
    BasicCourse,
    AccountId,
    CourseId,
)
from darwin.midtier.clients.moodle.moodle_client import MoodleClient
from darwin.models.client_models import MoodleCourse
import darwin.midtier.services.moodle_course_service as MoodleCourseService
from darwin.midtier.modules.authentication import ACCOUNT

router = APIRouter(
    prefix="/course",
    tags=["course"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
def get_all(account: ACCOUNT, all: bool = False) -> list[BasicCourse]:
    if not all:
        return CourseService.get_all_basic(account.id)
    if account.permission != AccountPermission.ADMIN:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "Must have admin permission to get all courses",
        )
    return CourseService.get_all_basic()


@router.get("/{course_id}")
def get(course_id: CourseId) -> Course:
    return CourseService.get(course_id)


@router.post("/moodle", status_code=201)
def createMoodle(moodle_course_create: MoodleCourseCreate) -> Course:
    moodle_course: MoodleCourse = MoodleClient(
        moodle_course_create.moodle_session,
    ).html_get_course(moodle_course_create.id)
    try:
        return MoodleCourseService.create(moodle_course)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
