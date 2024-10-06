from fastapi import APIRouter
from src.darwin.midtier.services.course import CourseService

router = APIRouter(
    prefix="/course",
    tags=["course"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
def get_courses():
    return CourseService.get_all(), 200
