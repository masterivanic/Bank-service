import datetime
from decimal import Decimal
from uuid import UUID

import attr

from bank_app.application.domain.domain_models import Account, AccountIdentity


@attr.dataclass(slots=True, hash=False, eq=False)
class BankAccount(Account):
    entity_id: "AccountIdentity"
    account_number: UUID
    balance: Decimal = Decimal("0.00")
    overdraft_amount: Decimal = Decimal("0.00")
    is_allow_overdraft: bool = True
    is_active: bool = True
    created_at: datetime.datetime = datetime.datetime.now()
    updated_at: datetime.datetime = datetime.datetime.now()

    def __attrs_post_init__(self):
        if not self.is_allow_overdraft:
            if self.balance < 0:
                raise ValueError("The balance cannot be negative")
        super().__attrs_post_init__()

    def deposit(self, amount: Decimal) -> None:
        if amount <= 0:
            raise ValueError("The deposit amount must be positive")
        self.balance += amount

        if self.balance < 0:
            raise ValueError("The balance cannot be negative")

    def withdraw(self, amount: Decimal) -> None:
        if amount <= 0:
            raise ValueError("The withdrawal amount must be positive")
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
            return self.available_balance >= amount
        return self.balance >= amount

    def set_overdraft_amount(self, amount: Decimal) -> None:
        """Set the overdraft authorization amount"""
        if amount < 0:
            raise ValueError("Overdraft authorization cannot be negative")
        self.overdraft_amount = amount
