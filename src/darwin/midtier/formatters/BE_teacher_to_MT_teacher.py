from darwin.models.backend_models import Teacher as BE_Teacher, Account as BE_Account
from darwin.models.midtier_models import Teacher as MT_Teacher


def BE_teacher_to_MT_teacher(
    BE_teacher: BE_Teacher, accounts: list[BE_Account]
) -> MT_Teacher:
    teachers_account: BE_Account
    for account in accounts:
        if BE_teacher.account_f == account.id:
            teachers_account = account
            break
    else:
        raise Exception(f"Failed to find teacher '{BE_teacher.id}' account")

    return MT_Teacher(
        id=BE_teacher.id,
        name=teachers_account.name,
        email=teachers_account.email,
    )
