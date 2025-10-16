from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

from domain.domain_models import DomainService

if TYPE_CHECKING:
    from domain.dtos.bank_account import BankAccountDTO


class BankAccount(DomainService):
    def redraw(self, account_number: UUID, amount: Decimal) -> "BankAccountDTO":
        """action to redraw money from bank account"""
        raise NotImplementedError

    def deposit_money(self, account_number: UUID, amount: Decimal) -> "BankAccountDTO":
        """action to put money in bank account"""
        raise NotImplementedError
