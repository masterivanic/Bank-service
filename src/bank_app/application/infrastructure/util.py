from decimal import Decimal
from enum import Enum


def validate_amount(amount: Decimal, message: str) -> None:
    if amount <= 0:
        raise ValueError(message)


class AccountType(Enum):
    CURRENT_ACCOUNT = "CURRENT_ACCOUNT"
    BOOKLET_ACCOUNT = "BOOKLET_ACCOUNT"
