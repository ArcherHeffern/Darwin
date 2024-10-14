from typing import cast
from fastapi import APIRouter, HTTPException, status
from regex import W
from darwin.midtier.services.course import CourseService
from darwin.models.backend_models import AccountPermission
from darwin.models.midtier_models import (
    MoodleCourseCreate,
    Course,
    BasicCourse,
    AccountId,
    CourseId,
)
from darwin.midtier.modules.authentication import (
    ACCOUNT,
    raise_if_not_admin,
    raise_if_unauthorized_create,
    raise_if_unauthorized_get,
)

router = APIRouter(
    prefix="/course",
    tags=["course"],
    responses={404: {"description": "Not found"}},
)


@router.get("/user/")
def get_all_courses_for_self(account: ACCOUNT):
    return CourseService.get_all_basic(account.id)


@router.get("/user/{account_id}")
def get_all_for_account(account: ACCOUNT, account_id: AccountId) -> list[BasicCourse]:
    raise_if_not_admin(account)
    return CourseService.get_all_basic(account_id)


@router.get("/")
def get_all() -> list[BasicCourse]:
    return CourseService.get_all_basic()


@router.get("/{course_id}")
def get(account: ACCOUNT, course_id: CourseId) -> Course:
    raise_if_unauthorized_get(account, course_id)
    return CourseService.get(course_id)


@router.post("/moodle", status_code=201)
def createMoodle(account: ACCOUNT, moodle_course_create: MoodleCourseCreate) -> Course:
    raise_if_unauthorized_create(account, AccountPermission.TA)
    return CourseService.create_moodle_course(account, moodle_course_create)
