from decimal import Decimal
from uuid import UUID

import attr

from domain.dtos.queries import DTO


@attr.dataclass(frozen=True, slots=True)
class BankAccountDTO(DTO):
    entity_id: UUID
    account_number: UUID
    balance: Decimal = Decimal(0)
