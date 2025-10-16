import abc
from decimal import Decimal
from uuid import UUID

from domain.domain_models import AbstractRepository
from domain.model.bank_account import AccountIdentity, BankAccount


class IBankAccountRepository(AbstractRepository):
    @classmethod
    @abc.abstractmethod
    def get(cls, entity_id: "AccountIdentity") -> BankAccount:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def get_by_bank_account_number(cls, account_number: UUID) -> BankAccount:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def delete(
        cls,
        entity_id: "AccountIdentity",
    ) -> None:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def save(cls, entity: "BankAccount") -> None:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def update_overdraft_amount(
        cls, account_number: UUID, overdraft_amount: Decimal
    ) -> None:
        raise NotImplementedError
