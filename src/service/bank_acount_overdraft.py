from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

from src.domain.dtos.bank_account import BankAccountDTO
from src.domain.exceptions import NotFound
from src.ports.api.bank_account_overdraft_use_case import BankAccountOverdraft

if TYPE_CHECKING:
    from src.domain.service.bank_account import BankAccountService
    from src.ports.repositories.i_bank_account import IBankAccountRepository


class BankAccountOverdraftService(BankAccountOverdraft):
    _bank_account_repository: "IBankAccountRepository"
    _bank_account_service: "BankAccountService"

    def __init__(
        self,
        bank_account_repository: "IBankAccountRepository",
        bank_account_service: "BankAccountService",
    ) -> None:
        self._bank_account_repository = bank_account_repository
        self._bank_account_service = bank_account_service

    def withdraw_from_account(
        self, account_number: UUID, amount: Decimal
    ) -> "BankAccountDTO":
        bank_account = self._bank_account_repository.get_by_bank_account_number(
            account_number=account_number
        )
        if not bank_account:
            raise NotFound(f"Account with number {account_number} not found")

        if amount <= 0:
            raise ValueError("cannot redraw null or negative amount")
        self._bank_account_service.authorize_withdrawal(
            account=bank_account, amount=amount
        )
        bank_account.withdraw(amount=amount)
        self._bank_account_repository.save(bank_account)
        return BankAccountDTO(
            entity_id=bank_account.entity_id.uuid,
            account_number=bank_account.account_number,
            balance=bank_account.balance,
        )

    def set_overdraft_amount(
        self, account_number: UUID, overdraft_amount: Decimal
    ) -> "BankAccountDTO":
        bank_account = self._bank_account_repository.get_by_bank_account_number(
            account_number=account_number
        )
        if not bank_account:
            raise NotFound(f"Account with number {account_number} not found")

        if overdraft_amount < 0:
            raise ValueError("cannot set overdraft with null or negative amount")

        bank_account.set_overdraft_amount(overdraft_amount)
        self._bank_account_repository.save(bank_account)
        return BankAccountDTO(
            entity_id=bank_account.entity_id.uuid,
            account_number=bank_account.account_number,
            balance=bank_account.balance,
            overdraft_amount=bank_account.overdraft_amount,
        )

    def get_available_balance(self, account_number: UUID) -> Decimal:
        bank_account = self._bank_account_repository.get_by_bank_account_number(
            account_number=account_number
        )
        if not bank_account:
            raise NotFound(f"Account with number {account_number} not found")
        return bank_account.available_balance
