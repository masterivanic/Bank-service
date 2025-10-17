import uuid
from decimal import Decimal

from src.domain.domain_models import AccountIdentity, DomainService
from src.domain.exceptions import (
    DepositLimitExceededException,
    InsufficientFundsException,
)
from src.domain.model.booklet_account import BookletAccount


class BookletAcountService(DomainService):
    @classmethod
    def create_account(
        cls, initial_deposit: Decimal, deposit_limit: Decimal
    ) -> "BookletAccount":
        return BookletAccount(
            entity_id=AccountIdentity(uuid.uuid4()),
            account_number=uuid.uuid4(),
            balance=initial_deposit,
            deposit_limit=deposit_limit,
        )

    @classmethod
    def can_deposit(cls, account: BookletAccount, amount: Decimal) -> bool:
        return (account.balance + amount) <= account.deposit_limit

    @classmethod
    def can_withdraw(cls, account: BookletAccount, amount: Decimal) -> bool:
        return account.has_sufficient_funds(amount)

    @classmethod
    def authorize_deposit(cls, account: BookletAccount, amount: Decimal) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")

        new_balance = account.balance + amount
        if new_balance > account.deposit_limit:
            raise DepositLimitExceededException("Deposit would exceed deposit limit")

    @classmethod
    def authorize_withdrawal(cls, account: BookletAccount, amount: Decimal) -> None:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")

        if not account.has_sufficient_funds(amount):
            raise InsufficientFundsException(
                f"Insufficient funds for withdrawal of {amount}"
            )
