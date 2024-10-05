from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/account",
    tags=["account"],
    responses={404: {"description": "Not found"}},
)