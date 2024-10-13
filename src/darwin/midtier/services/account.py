from datetime import datetime, timedelta

from bcrypt import gensalt, hashpw
from darwin.config import Config
from uuid import uuid4
from fastapi import HTTPException, status
from darwin.models.backend_models import (
    AccountId,
    AccountCreateToken,
    AccountCreateTokenId,
    AccountStatus,
)
from darwin.models.midtier_models import (
    Account as MT_Account,
    AccountCreateP1,
    AccountCreateP1Response,
    AccountCreateP2,
)
from darwin.midtier.formatters import account_formatter
from darwin.backend import Backend
from darwin.midtier.clients.gmail import Gmail

account_dal = Backend.account_dal
account_create_token_dal = Backend.account_create_token_dal


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
            "Darwin Email Verification",
            f"Verify this is your email: {Config.WEB_HOST}/account/verify/{account_create_token.id}",
        )

        return AccountCreateP1Response(ttl=Config.ACCOUNT_CREATE_TOKEN_EXPR_TIME)

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
