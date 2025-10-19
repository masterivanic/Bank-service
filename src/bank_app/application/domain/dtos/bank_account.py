from decimal import Decimal
from typing import Optional
from uuid import UUID

import attr

from bank_app.application.domain.dtos.queries import DTO


@attr.dataclass(frozen=True, slots=True)
class BankAccountDTO(DTO):
    entity_id: UUID
    account_number: UUID
    balance: Decimal
    overdraft_amount: Optional[Decimal] = None
