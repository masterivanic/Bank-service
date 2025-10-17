import abc
from typing import Any
from uuid import UUID

from bank_app.application.domain.domain_models import (
    AbstractRepository,
    AccountIdentity,
    Entity,
    EntityIdentity,
)
from bank_app.application.domain.model.booklet_account import BookletAccount


class IBookletAccountRepository(AbstractRepository):
    @classmethod
    @abc.abstractmethod
    def get(cls, entity_id: EntityIdentity) -> BookletAccount:
        if not isinstance(entity_id, AccountIdentity):
            raise ValueError("entity_id must be an AccountIdentity")
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def get_by_booklet_account_number(cls, account_number: UUID) -> BookletAccount:
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
        if not isinstance(entity, BookletAccount):
            raise ValueError("entity must be a BookletAccount")
        raise NotImplementedError
