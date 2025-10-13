from decimal import Decimal


def validate_amount(amount: Decimal, message: str):
    if amount == 0 and amount < 0:
        raise ValueError(message)
