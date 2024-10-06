from fastapi import APIRouter
from darwin.midtier.services.assignment import AssignmentService


router = APIRouter(
    prefix='/assignment',
    tags=['assignment'],
    responses={404: {"description": "Not found"}},
    )

@router.get('/')
def get_assignments():
    return AssignmentService.get_all(), 200