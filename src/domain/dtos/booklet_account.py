from decimal import Decimal
from uuid import UUID

import attr

from src.domain.dtos.queries import DTO
from src.domain.model.booklet_account import BookletAccount


@attr.dataclass(frozen=True, slots=True)
class BookletAccountDTO(DTO):
    entity_id: UUID
    account_number: UUID
    balance: Decimal
    deposit_limit: Decimal
    is_active: bool
    remaining_deposit_capacity: Decimal

    @classmethod
    def from_entity(cls, account: BookletAccount) -> "BookletAccountDTO":
        return cls(
            entity_id=account.entity_id.uuid,
            account_number=account.account_number,
            balance=account.balance,
            deposit_limit=account.deposit_limit,
            is_active=account.is_active,
            remaining_deposit_capacity=account.get_remaining_deposit_capacity(),
        )
