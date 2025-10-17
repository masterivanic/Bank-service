import datetime
from decimal import Decimal
from uuid import UUID

import attr

from src.domain.dtos.queries import DTO
from src.domain.model.account_statement import MonthlyStatement, Transaction


@attr.dataclass(frozen=True, slots=True)
class MonthlyStatementDTO(DTO):
    account_id: UUID
    account_type: str
    account_number: UUID
    generated_at: datetime.datetime
    opening_balance: Decimal
    closing_balance: Decimal
    transactions: list[Transaction]

    @classmethod
    def from_entity(cls, monthly_statement: MonthlyStatement) -> "MonthlyStatementDTO":
        return cls(
            account_id=monthly_statement.account_id,
            account_type=monthly_statement.account_type,
            account_number=monthly_statement.account_number,
            generated_at=monthly_statement.generated_at,
            opening_balance=monthly_statement.opening_balance,
            closing_balance=monthly_statement.closing_balance,
            transactions=monthly_statement.transactions,
        )
