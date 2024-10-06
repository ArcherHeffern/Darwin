from fastapi import APIRouter
from src.darwin.backend import Backend

router = APIRouter(
    prefix='/course',
    tags=['course'],
    responses={404: {"description": "Not found"}},
    )

@router.get('/')
def get_courses():
    return Backend.course_service.get_all(), 200