from decimal import Decimal


def validate_amount(amount: Decimal, message: str) -> None:
    if amount <= 0:
        raise ValueError(message)
