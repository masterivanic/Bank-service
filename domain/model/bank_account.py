import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

import attr

from domain.domain_models import Entity, EntityIdentity
from domain.exceptions import BusinessException


@attr.dataclass(frozen=True, slots=True)
class BankAccountIdentity(EntityIdentity):
    uuid: UUID


@attr.dataclass(slots=True, hash=False, eq=False)
class BankAccount(Entity):
    entity_id: "BankAccountIdentity"
    account_number: UUID
    balance: Decimal
    overdraft_amount: Decimal = Decimal("0.00")
    is_allow_overdraft: bool = True
    is_active: Optional[bool] = True
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None

    def __attrs_post_init__(self):
        if self.balance < 0:
            raise ValueError("The balance cannot be negative")

    def deposit(self, amount: Decimal) -> None:
        if amount <= 0:
            raise ValueError("The deposit amount must be positive")
        self.balance += amount

    def withdraw(self, amount: Decimal) -> None:
        if amount <= 0:
            raise ValueError("The withdrawal amount must be positive")

        if amount > self.balance:
            raise BusinessException("Insufficient funds to make this withdrawal")

        self.balance -= amount

    def is_in_overdraft(self) -> bool:
        return self.balance < 0

    def get_overdraft_used(self) -> Decimal:
        return (
            max(Decimal("0.00"), -self.balance) if self.balance < 0 else Decimal("0.00")
        )

    @property
    def available_balance(self) -> Decimal:
        if self.is_allow_overdraft:
            return self.balance + self.overdraft_amount
        return self.balance

    def has_sufficient_funds(self, amount: Decimal) -> bool:
        if self.is_allow_overdraft:
            available_balance = self.balance + self.overdraft_amount
            return available_balance >= amount
        return self.balance >= amount

    def set_overdraft_amount(self, amount: Decimal) -> None:
        """Set the overdraft authorization amount"""
        if amount < 0:
            raise ValueError("Overdraft authorization cannot be negative")
        self.overdraft_amount = amount
