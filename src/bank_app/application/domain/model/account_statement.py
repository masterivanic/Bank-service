import datetime
from decimal import Decimal
from uuid import UUID

import attr

from bank_app.application.domain.domain_models import (
    AccountIdentity,
    Entity,
    EntityIdentity,
)


@attr.dataclass(frozen=True, slots=True)
class TransactionIdentity(EntityIdentity):
    uuid: UUID


@attr.dataclass(frozen=True, slots=True)
class MonthlyStatementIdentity(EntityIdentity):
    uuid: UUID


@attr.dataclass(frozen=True, slots=True)
class AccountType:
    CURRENT_ACCOUNT = "CURRENT_ACCOUNT"  # COMPTE COURANT
    BOOKLET_ACCOUNT = "BOOKLET_ACCOUNT"  # LIVRET A


@attr.dataclass(slots=True, hash=False, eq=False)
class Transaction(Entity):
    entity_id: "TransactionIdentity"
    account_id: "AccountIdentity"
    account_type: str  # CURRENT_ACCOUNT, BOOKLET_ACCOUNT
    transaction_type: str  # "DEPOSIT", "WITHDRAWAL"
    amount: Decimal
    transation_date: datetime.datetime


@attr.dataclass(slots=True, hash=False, eq=False)
class MonthlyStatement(Entity):
    """
    monthly account statement
    """

    entity_id: "MonthlyStatementIdentity"
    account_id: UUID
    account_type: str
    account_number: UUID
    period_start: datetime.datetime
    period_end: datetime.datetime
    generated_at: datetime.datetime
    opening_balance: Decimal
    closing_balance: Decimal
    transactions: list[Transaction]

    @property
    def total_deposits(self) -> Decimal:
        return sum(
            (t.amount for t in self.transactions if t.transaction_type == "DEPOSIT"),
            Decimal(0),
        )

    @property
    def total_withdrawals(self) -> Decimal:
        return sum(
            (t.amount for t in self.transactions if t.transaction_type == "WITHDRAWAL"),
            Decimal(0),
        )
