from fastapi import APIRouter
from src.darwin.backend.dal.dal import assignment_dal as assignment

router = APIRouter(
    prefix='/assignment',
    tags=['assignment'],
    responses={404: {"description": "Not found"}},
    )

@router.get('/')
def get_assignments():
    return assignment.get_all(), 200