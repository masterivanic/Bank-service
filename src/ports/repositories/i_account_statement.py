import abc
from typing import Any
from uuid import UUID

from src.domain.domain_models import (
    AbstractRepository,
    Entity,
    EntityIdentity,
)
from src.domain.model.account_statement import (
    MonthlyStatement,
    MonthlyStatementIdentity,
)


class IAccountStatementRepository(AbstractRepository):
    @classmethod
    @abc.abstractmethod
    def get(cls, entity_id: EntityIdentity) -> MonthlyStatement:
        if not isinstance(entity_id, MonthlyStatementIdentity):
            raise ValueError("entity_id must be an MonthlyStatementIdentity")
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def get_by_account_number(cls, account_number: UUID) -> MonthlyStatement:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def delete(cls, entity_id: EntityIdentity, **kwargs: Any) -> None:
        if not isinstance(entity_id, MonthlyStatementIdentity):
            raise ValueError("entity_id must be an MonthlyStatementIdentity")
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def save(cls, entity: Entity) -> None:
        if not isinstance(entity, MonthlyStatement):
            raise ValueError("entity must be a MonthlyStatement")
        raise NotImplementedError
