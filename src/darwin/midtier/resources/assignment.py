from fastapi import APIRouter
from darwin.midtier.services.assignment import AssignmentService
from darwin.models.midtier_models import (
    Assignment,
    BasicAssignment,
    CreateAssignment,
    CourseId,
    AssignmentId,
)
from typing import Optional


router = APIRouter(
    prefix="/assignment",
    tags=["assignment"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{assignment_id}")
def get_assignment(assignment_id: AssignmentId) -> Assignment:
    return AssignmentService.get(assignment_id)


@router.get("/")
def get_assignments(
    course_id: Optional[CourseId] = None, hide_deleted: bool = True
) -> list[BasicAssignment]:
    return AssignmentService.get_all(course_id, hide_deleted=hide_deleted)


@router.post("/", status_code=201)
def create_assignment(assignment: CreateAssignment) -> Assignment:
    return AssignmentService.create(assignment)
