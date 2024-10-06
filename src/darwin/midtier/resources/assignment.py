from fastapi import APIRouter
from src.darwin.backend.dal import Dal


router = APIRouter(
    prefix='/assignment',
    tags=['assignment'],
    responses={404: {"description": "Not found"}},
    )

@router.get('/')
def get_assignments():
    return Dal.assignment_dal.get_all(), 200