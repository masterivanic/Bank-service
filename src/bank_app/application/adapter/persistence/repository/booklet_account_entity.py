from typing import Any
from uuid import UUID

from bank_app.application.adapter.persistence.entity.booklet_account_entity import (
    BookletAccountEntity,
)
from bank_app.application.domain.domain_models import (
    AccountIdentity,
    Entity,
    EntityIdentity,
)
from bank_app.application.domain.exceptions import NotFound
from bank_app.application.domain.model.booklet_account import BookletAccount
from bank_app.application.ports.repositories.i_booklet_account import (
    IBookletAccountRepository,
)


class BookletAccountRepository(IBookletAccountRepository):
    @classmethod
    def _get_booklet_account_by_id(
        cls, entity_id: AccountIdentity
    ) -> BookletAccountEntity:
        try:
            return BookletAccountEntity.objects.get(entity_id=entity_id.uuid)
        except BookletAccountEntity.DoesNotExist as ex:
            raise NotFound(f"Booklet account {entity_id.uuid} does not exist") from ex

    @classmethod
    def _get_booklet_account_by_account_number(
        cls, account_number: UUID
    ) -> BookletAccountEntity:
        try:
            return BookletAccountEntity.objects.get(account_number=account_number)
        except BookletAccountEntity.DoesNotExist as ex:
            raise NotFound(
                f"Booklet account with number {account_number} does not exist"
            ) from ex

    @classmethod
    def _to_domain(cls, entity: BookletAccountEntity) -> BookletAccount:
        return BookletAccount(
            entity_id=AccountIdentity(entity.entity_id),
            account_number=entity.account_number,
            balance=entity.balance,
            deposit_limit=entity.deposit_limit,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    @classmethod
    def _to_entity(cls, domain: BookletAccount) -> BookletAccountEntity:
        try:
            entity = BookletAccountEntity.objects.get(entity_id=domain.entity_id.uuid)
            entity.account_number = domain.account_number
            entity.balance = domain.balance
            entity.deposit_limit = domain.deposit_limit
            entity.is_active = domain.is_active
            return entity
        except BookletAccountEntity.DoesNotExist:
            return BookletAccountEntity(
                entity_id=domain.entity_id.uuid,
                account_number=domain.account_number,
                balance=domain.balance,
                deposit_limit=domain.deposit_limit,
                is_active=domain.is_active,
            )

    @classmethod
    def get(cls, entity_id: EntityIdentity) -> BookletAccount:
        if not isinstance(entity_id, AccountIdentity):
            raise ValueError("entity_id must be an AccountIdentity")

        booklet_account_entity = cls._get_booklet_account_by_id(entity_id)
        return cls._to_domain(booklet_account_entity)

    @classmethod
    def get_by_booklet_account_number(cls, account_number: UUID) -> BookletAccount:
        booklet_account_entity = cls._get_booklet_account_by_account_number(
            account_number
        )
        return cls._to_domain(booklet_account_entity)

    @classmethod
    def delete(cls, entity_id: EntityIdentity, **kwargs: Any) -> None:
        if not isinstance(entity_id, AccountIdentity):
            raise ValueError("entity_id must be an AccountIdentity")

        booklet_account_entity = cls._get_booklet_account_by_id(entity_id)
        booklet_account_entity.delete()

    @classmethod
    def save(cls, entity: Entity) -> None:
        if not isinstance(entity, BookletAccount):
            raise ValueError("entity must be a BookletAccount")

        booklet_account_entity = cls._to_entity(entity)
        booklet_account_entity.save()
