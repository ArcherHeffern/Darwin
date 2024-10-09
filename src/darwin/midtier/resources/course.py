from fastapi import APIRouter, HTTPException
from darwin.midtier.services.course import CourseService
from darwin.models.midtier_models import BasicAssignment, MoodleCourseCreate, Course, BasicCourse, AccountId
from darwin.midtier.clients.moodle.moodle_client import MoodleClient
from darwin.models.client_models import MoodleCourse
import darwin.midtier.services.moodle_course_service as MoodleCourseService

router = APIRouter(
    prefix="/course",
    tags=["course"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
def get_all(account_id: AccountId) -> list[BasicCourse]:
    return CourseService.get_all_basic(account_id)


@router.post("/moodle", status_code=201)
def createMoodle(moodle_course_create: MoodleCourseCreate) -> Course:
    moodle_course: MoodleCourse = MoodleClient(
        moodle_course_create.moodle_session,
    ).html_get_course(moodle_course_create.id)
    try:
        return MoodleCourseService.create(moodle_course)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

