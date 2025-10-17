import uuid
from decimal import Decimal

from src.domain.domain_models import AccountIdentity, DomainService
from src.domain.exceptions import (
    InsufficientFundsException,
    OverdraftLimitExceededException,
)
from src.domain.model.bank_account import BankAccount


class BankAccountService(DomainService):
    @classmethod
    def create_account(cls, initial_balance: Decimal) -> "BankAccount":
        return BankAccount(
            entity_id=AccountIdentity(uuid.uuid4()),
            account_number=uuid.uuid4(),
            balance=initial_balance,
        )

    @classmethod
    def can_withdraw(cls, account: BankAccount, amount: Decimal) -> bool:
        return account.has_sufficient_funds(amount=amount)

    @classmethod
    def authorize_withdrawal(cls, account: BankAccount, amount: Decimal) -> None:
        """authorize Withdrawal considering  overdraft authorization"""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")

        if not account.has_sufficient_funds(amount):
            if account.overdraft_amount > 0:
                raise OverdraftLimitExceededException(
                    f"Withdrawal of {amount} exceeds overdraft limit."
                )
            raise InsufficientFundsException(
                f"Insufficient funds for withdrawal of {amount}"
            )
