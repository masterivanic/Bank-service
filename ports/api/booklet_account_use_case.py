from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

from domain.domain_models import DomainService

if TYPE_CHECKING:
    from domain.dtos.booklet_account import BookletAccountDTO


class BookletAccount(DomainService):
    def redraw(self, account_number: UUID, amount: Decimal) -> "BookletAccountDTO":
        """action to redraw money from bank account"""
        raise NotImplementedError

    def deposit_money(
        self, account_number: UUID, amount: Decimal
    ) -> "BookletAccountDTO":
        """action to put money in bank account"""
        raise NotImplementedError

    def update_deposit_limit(
        self, account_number: UUID, amount: Decimal
    ) -> "BookletAccountDTO":
        """action to update deposit limit of bank account"""
        raise NotImplementedError
