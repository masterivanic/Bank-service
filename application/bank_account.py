from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

from domain.dtos.bank_account import BankAccountDTO
from domain.exceptions import BusinessException, NotFound
from domain.service.bank_account import BankAccountService
from ports.api.bank_account_use_case import BankAccount

if TYPE_CHECKING:
    from ports.repositories.i_bank_account import IBankAccountRepository


class BankAccountRedrawAndDepositService(BankAccount):
    _bank_account_repository: "IBankAccountRepository"

    def __init__(self, bank_account_repository: "IBankAccountRepository"):
        self._bank_account_repository = bank_account_repository

    def redraw(self, account_number: UUID, amount: Decimal) -> "BankAccountDTO":
        bank_account = self._bank_account_repository.get_by_bank_account_number(
            account_number=account_number
        )
        if not bank_account:
            raise NotFound(f"Account with number {account_number} not found")

        if amount == 0 or amount < 0:
            raise ValueError("cannot redraw null or negative amount")

        if not BankAccountService.can_withdraw(bank_account, amount) and amount > 0:
            raise BusinessException("Insufficient funds to make this withdrawal")

        bank_account.withdraw(amount=amount)
        self._bank_account_repository.save(bank_account)
        return BankAccountDTO(
            entity_id=bank_account.entity_id,
            account_number=bank_account.account_number,
            balance=bank_account.balance,
        )

    def deposit_money(self, account_number, amount) -> "BankAccountDTO":
        bank_account = self._bank_account_repository.get_by_bank_account_number(
            account_number=account_number
        )
        if not bank_account:
            raise NotFound(f"Account with number {account_number} not found")

        if amount == 0 or amount < 0:
            raise ValueError("cannot deposit null or negative amount")

        bank_account.deposit(amount)
        self._bank_account_repository.save(bank_account)
        return BankAccountDTO(
            entity_id=bank_account.entity_id,
            account_number=bank_account.account_number,
            balance=bank_account.balance,
        )
