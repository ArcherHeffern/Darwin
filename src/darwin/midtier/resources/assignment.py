from fastapi import APIRouter
from darwin.midtier.modules.authentication import ACCOUNT, raise_if_not_admin, raise_if_unauthorized_get, raise_if_unauthorized_modify
from darwin.midtier.services.assignment import AssignmentService
from darwin.models.backend_models import AccountPermission
from darwin.models.midtier_models import (
    Assignment,
    BasicAssignment,
    CreateAssignment,
    CourseId,
    AssignmentId,
)


router = APIRouter(
    prefix="/assignment",
    tags=["assignment"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{assignment_id}")
def get_assignment(account: ACCOUNT, assignment_id: AssignmentId) -> Assignment:
    raise_if_unauthorized_get(account, assignment_id)
    return AssignmentService.get(assignment_id)


@router.get("/course/{course_id}")
def get_assignments_by_course(
    account: ACCOUNT, course_id: CourseId, hide_deleted: bool = True
) -> list[BasicAssignment]:
    raise_if_unauthorized_get(account, course_id)
    return AssignmentService.get_all(course_id, hide_deleted=hide_deleted)


@router.get("/")
def get_assignments(account: ACCOUNT, hide_deleted: bool = True) -> list[BasicAssignment]:
    raise_if_not_admin(account)
    return AssignmentService.get_all(hide_deleted=hide_deleted)



@router.post("/", status_code=201)
def create_assignment(account: ACCOUNT, assignment: CreateAssignment) -> Assignment:
    raise_if_unauthorized_modify(account, assignment.course_f)
    return AssignmentService.create(assignment)
