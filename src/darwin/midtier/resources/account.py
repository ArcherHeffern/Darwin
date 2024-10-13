from typing import Optional
from fastapi import APIRouter, HTTPException, status
from darwin.models.midtier_models import (
    AccountCreateP1,
    AccountCreateP1Response,
    AccountCreateP2,
    AccountId,
    Account as MT_Account,
)
from darwin.models.backend_models import Account as BE_Account, AccountPermission, AccountCreateTokenId
from darwin.midtier.services.account import AccountService
from darwin.midtier.modules.authentication import ACCOUNT

router = APIRouter(
    prefix="/account",
    tags=["account"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{account_id}")
def get_account(account: ACCOUNT, account_id: Optional[AccountId] = None) -> MT_Account:
    if account_id is None or account_id == account.id:
        return account
    if account.permission != AccountPermission.ADMIN:
        return AccountService.get_by_id(account_id)
    raise HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        "Must be admin to fetch others account information",
    )


@router.get("/")
def get_accounts(account: ACCOUNT) -> list[MT_Account]:
    if account.permission != AccountPermission.ADMIN:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "Must be admin to fetch others account information",
        )
    return AccountService.get_all()


@router.post("/signup")
def signup(account_create: AccountCreateP1) -> AccountCreateP1Response:
    return AccountService.create_p1(account_create)


@router.post("/verify_email/{token}")
def verify_email(token: AccountCreateTokenId, account_create: AccountCreateP2) -> MT_Account:
    return AccountService.create_p2(token, account_create)


def upgrade_account(account_id: AccountId, account_permission: AccountPermission): ...


@router.get("/login")
def login(): ...


def logout(): ...
