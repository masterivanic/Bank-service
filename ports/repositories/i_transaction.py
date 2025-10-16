import abc
from typing import Any

from domain.domain_models import (
    AbstractRepository,
    AccountIdentity,
    Entity,
    EntityIdentity,
)
from domain.model.account_statement import Transaction, TransactionIdentity


class ITransactionRepository(AbstractRepository):
    @classmethod
    @abc.abstractmethod
    def get(cls, entity_id: EntityIdentity) -> Transaction:
        if not isinstance(entity_id, TransactionIdentity):
            raise ValueError("entity_id must be an TransactionIdentity")
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def get_by_account_id(cls, account_id: AccountIdentity) -> list[Transaction]:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def delete(cls, entity_id: EntityIdentity, **kwargs: Any) -> None:
        if not isinstance(entity_id, TransactionIdentity):
            raise ValueError("entity_id must be an TransactionIdentity")
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def save(cls, entity: Entity) -> None:
        if not isinstance(entity, Transaction):
            raise ValueError("entity must be a Transaction")
        raise NotImplementedError
