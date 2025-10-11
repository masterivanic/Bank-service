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

    def has_sufficient_funds(self, amount: Decimal) -> bool:
        return self.balance >= amount
