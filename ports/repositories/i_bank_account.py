import abc
from decimal import Decimal
from typing import Any
from uuid import UUID

from domain.domain_models import (
    AbstractRepository,
    AccountIdentity,
    Entity,
    EntityIdentity,
)
from domain.model.bank_account import BankAccount


class IBankAccountRepository(AbstractRepository):
    @classmethod
    @abc.abstractmethod
    def get(cls, entity_id: EntityIdentity) -> BankAccount:
        if not isinstance(entity_id, AccountIdentity):
            raise ValueError("entity_id must be an AccountIdentity")
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def get_by_bank_account_number(cls, account_number: UUID) -> BankAccount:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def delete(cls, entity_id: EntityIdentity, **kwargs: Any) -> None:
        if not isinstance(entity_id, AccountIdentity):
            raise ValueError("entity_id must be an AccountIdentity")
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def save(cls, entity: Entity) -> None:
        if not isinstance(entity, BankAccount):
            raise ValueError("entity must be a BankAccount")
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def update_overdraft_amount(
        cls, account_number: UUID, overdraft_amount: Decimal
    ) -> None:
        raise NotImplementedError
