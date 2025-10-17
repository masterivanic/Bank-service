from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

from src.domain.domain_models import DomainService

if TYPE_CHECKING:
    from src.domain.dtos.bank_account import BankAccountDTO


class BankAccountOverdraft(DomainService):
    def withdraw_from_account(
        self, account_number: UUID, amount: Decimal
    ) -> "BankAccountDTO":
        """Withdraw money from account considering overdraft authorization"""
        raise NotImplementedError

    def set_overdraft_amount(
        self, account_number: UUID, overdraft_amount: Decimal
    ) -> "BankAccountDTO":
        """Set overdraft authorization for an account"""
        raise NotImplementedError

    def get_available_balance(self, account_number: UUID) -> Decimal:
        """Get available balance including overdraft authorization"""
        raise NotImplementedError
