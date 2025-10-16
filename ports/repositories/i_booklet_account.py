import abc
from uuid import UUID

from domain.domain_models import AbstractRepository, AccountIdentity
from domain.model.booklet_account import BookletAccount


class IBookletAccountRepository(AbstractRepository):
    @classmethod
    @abc.abstractmethod
    def get(cls, entity_id: "AccountIdentity") -> BookletAccount:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def get_by_booklet_account_number(cls, account_number: UUID) -> BookletAccount:
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
    def save(cls, entity: "BookletAccount") -> None:
        raise NotImplementedError
