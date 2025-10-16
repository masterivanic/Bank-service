import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

import attr

from domain.domain_models import Account, AccountIdentity
from domain.exceptions import (
    BusinessException,
    DepositLimitExceededException,
    InsufficientFundsException,
)


@attr.dataclass(slots=True, hash=False, eq=False)
class BookletAccount(Account):
    entity_id: "AccountIdentity"
    account_number: UUID
    balance: Decimal = Decimal("0.00")
    deposit_limit: Decimal = Decimal("22950.00")
    is_active: Optional[bool] = True
    created_at: Optional[datetime.datetime] = datetime.datetime.now()
    updated_at: Optional[datetime.datetime] = datetime.datetime.now()

    def __attrs_post_init__(self):
        super().__attrs_post_init__()

    def _validate_initial_state(self):
        if self.balance > self.deposit_limit:
            raise ValueError("Balance cannot exceed deposit limit")

    def deposit(self, amount: Decimal) -> None:
        if amount <= 0:
            raise ValueError("The deposit amount must be positive")

        new_balance = self.balance + amount
        if new_balance > self.deposit_limit:
            raise DepositLimitExceededException("Deposit limit has exceed")
        self.balance = new_balance

    def withdraw(self, amount: Decimal) -> None:
        if amount <= 0:
            raise ValueError("The withdrawal amount must be positive")

        if amount > self.balance:
            raise InsufficientFundsException(
                f"Insufficient funds for withdrawal of {amount}"
            )

        self.balance -= amount

    @property
    def available_balance(self) -> Decimal:
        return self.balance

    def has_sufficient_funds(self, amount: Decimal) -> bool:
        return self.balance >= amount

    def set_deposit_limit(self, new_limit: Decimal) -> None:
        if new_limit <= 0:
            raise ValueError("Deposit limit must be positive")

        if self.balance > new_limit:
            raise BusinessException(f"Cannot set deposit limit to {new_limit}")

        self.deposit_limit = new_limit

    def get_remaining_deposit_capacity(self) -> Decimal:
        return max(Decimal("0.00"), self.deposit_limit - self.balance)
