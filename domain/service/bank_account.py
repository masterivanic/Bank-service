import uuid
from decimal import Decimal

from domain.domain_models import DomainService
from domain.dtos.bank_account import BankAccountDTO
from domain.model.bank_account import BankAccount


class BankAccountService(DomainService):
    @classmethod
    def create_account(cls, initial_balance: Decimal) -> BankAccountDTO:
        raise BankAccountDTO(
            entity_id=uuid.uuid4(), account_number=uuid.uuid4(), balance=initial_balance
        )

    @classmethod
    def can_withdraw(cls, account: BankAccount, amount: Decimal) -> bool:
        return account.has_sufficient_funds(amount=amount)
