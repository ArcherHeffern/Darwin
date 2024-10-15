from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from darwin.backend import Backend
from darwin.models.midtier_models import (
    AccountCreateP1,
    AccountCreateP1Response,
    AccountCreateP2,
    LoginResponse,
    AccountId,
    Account as MT_Account,
    AuthTokenId,
    AuthTokenVerify,
)
from darwin.models.backend_models import (
    Account as BE_Account,
    AccountPermission,
    AccountCreateTokenId,
)
from darwin.midtier.services.account import AccountService
from darwin.midtier.modules.authentication import ACCOUNT, raise_if_not_admin

router = APIRouter(
    prefix="/account",
    tags=["account"],
    responses={404: {"description": "Not found"}},
)


@router.get("/user")
def get_my_account(account: ACCOUNT) -> MT_Account:
    return AccountService.get_by_id(account.id)


@router.get("/user/{account_id}")
def get_any_account(account: ACCOUNT, account_id: AccountId) -> MT_Account:
    raise_if_not_admin(account)
    return AccountService.get_by_id(account_id)


@router.get("/")
def get_accounts(account: ACCOUNT) -> list[MT_Account]:
    raise_if_not_admin(account)
    return AccountService.get_all()


@router.post("/signup")
def signup(account_create: AccountCreateP1) -> AccountCreateP1Response:
    return AccountService.create_p1(account_create)


@router.post("/verify_email/{token}")
def verify_email(
    token: AccountCreateTokenId, account_create: AccountCreateP2
) -> MT_Account:
    return AccountService.create_p2(token, account_create)


@router.post("/verify_token")
def verify_token(token: AuthTokenVerify):
    AccountService.verify_token(token.auth_token)

def upgrade_account(account_id: AccountId, account_permission: AccountPermission): ...


@router.post("/login")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> LoginResponse:
    return AccountService.login(form_data.username, form_data.password)


@router.post("/logout")
def logout(account: ACCOUNT): 
    AccountService.logout(account.id)
    
