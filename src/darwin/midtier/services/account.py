from datetime import datetime, timedelta
from darwin.config import Config

from darwin.midtier.formatters import auth_token_formatter
from bcrypt import gensalt, hashpw, checkpw
from darwin.config import Config
from uuid import uuid4
from fastapi import HTTPException, status
from darwin.models.backend_models import (
    AccountId,
    AccountCreateToken,
    AccountCreateTokenId,
    AccountStatus,
    AuthToken as BE_AuthToken,
    AuthTokenId,
)
from darwin.models.midtier_models import (
    Account as MT_Account,
    AccountCreateP1,
    AccountCreateP1Response,
    AccountCreateP2,
    LoginResponse,
    AuthToken as MT_AuthToken,
)
from darwin.midtier.formatters import account_formatter
from darwin.backend import Backend
from darwin.midtier.clients.gmail import Gmail

account_dal = Backend.account_dal
account_create_token_dal = Backend.account_create_token_dal
auth_token_dal = Backend.auth_token_dal


class AccountService:
    @staticmethod
    def get_by_id(account_id: AccountId) -> MT_Account:
        BE_account = account_dal.get(account_id)
        if BE_account is None:
            raise HTTPException(404, "Account not found")
        return account_formatter.BE_2_MT(BE_account)

    @staticmethod
    def get_all() -> list[MT_Account]:
        BE_accounts = account_dal.get_all()
        return [account_formatter.BE_2_MT(BE_account) for BE_account in BE_accounts]

    @staticmethod
    def create_p1(account_create: AccountCreateP1) -> AccountCreateP1Response:
        """
        Check if account already exists

        If not, send email verification
        """
        maybe_existing_account = account_dal.get_by_email(account_create.email)
        if (
            maybe_existing_account
            and maybe_existing_account.status == AccountStatus.REGISTERED
        ):
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                f"Account with email {maybe_existing_account.email} already exists",
            )

        account_create_token = AccountCreateToken(
            id=AccountCreateTokenId(str(uuid4())),
            email=account_create.email,
            expiration=datetime.now() + Config.ACCOUNT_CREATE_TOKEN_EXPR_TIME,
        )
        account_create_token_dal.create(account_create_token)

        # Send email
        Gmail.send(
            account_create.email,
            f"{Config.PROGRAM_NAME} Email Verification",
            f"Verify this is your email: {Config.VERIFY_EMAIL_URL}/{account_create_token.id}\n\nIf this was not you, ignore this email",
        )

        return AccountCreateP1Response(ttl=str(Config.ACCOUNT_CREATE_TOKEN_EXPR_TIME))


    @staticmethod
    def create_p2(
        token: AccountCreateTokenId, account_create: AccountCreateP2
    ) -> MT_Account:
        maybe_account_create_token = account_create_token_dal.get(token)

        if maybe_account_create_token is None:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND, "Account Creation Token Not Found"
            )
        if maybe_account_create_token.expiration < datetime.now():
            raise HTTPException(status.HTTP_408_REQUEST_TIMEOUT, "Token is expired")

        maybe_existing_account = account_dal.get_by_email(
            maybe_account_create_token.email
        )
        if maybe_existing_account:
            maybe_existing_account.status = AccountStatus.REGISTERED
            maybe_existing_account.name = account_create.name
            maybe_existing_account.hashed_password = hashpw(
                account_create.password.encode(), gensalt()
            ).decode()
            account_dal.update(maybe_existing_account)
            BE_account = maybe_existing_account
        else:
            BE_account = account_formatter.AccountCreateP2_2_BE(
                maybe_account_create_token.email, account_create
            )
            account_dal.create(BE_account)

        account_create_token_dal.delete_all(email=maybe_account_create_token.email)

        return account_formatter.BE_2_MT(BE_account)


    @staticmethod
    def login(username: str, password: str) -> LoginResponse:
        db_account = account_dal.get_by_email(username)
        if db_account is None or db_account.status != AccountStatus.REGISTERED:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        if db_account.hashed_password is None:
            raise Exception(
                f"Expected active account (id={db_account.id}) to contain hashed_password attribute but found None"
            )
        if not checkpw(password.encode(), db_account.hashed_password.encode()):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED)
        auth_token_id = AuthTokenId(str(uuid4()))
        BE_auth_token = BE_AuthToken(
            token=auth_token_id,
            account_f=db_account.id,
            expiration=datetime.now() + Config.AUTH_TOKEN_EXPIRATION,
            revoked=False,
        )
        auth_token_dal.delete_by_account(db_account.id)
        auth_token_dal.create(BE_auth_token)
        return LoginResponse(
            access_token=auth_token_id,
            account_id=db_account.id,
            expiration=BE_auth_token.expiration,
            name=db_account.name,
            permission=db_account.permission,
        )
    
    @staticmethod
    def logout(account_id: AccountId):
        auth_token_dal.delete_by_account(account_id)
    
    @staticmethod
    def verify_token(token: AuthTokenId):
        maybe_auth_token = auth_token_dal.get(token)
        if maybe_auth_token is None:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND, "Account Creation Token Not Found"
            )

        if maybe_auth_token.expiration < datetime.now():
            raise HTTPException(status.HTTP_408_REQUEST_TIMEOUT, "Token is expired")
        
