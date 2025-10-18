from decimal import Decimal
from typing import Any
from uuid import UUID

from bank_app.application.adapter.persistence.entity.bank_account_entity import (
    BankAccountEntity,
)
from bank_app.application.domain.domain_models import (
    AccountIdentity,
    Entity,
    EntityIdentity,
)
from bank_app.application.domain.exceptions import NotFound
from bank_app.application.domain.model.bank_account import BankAccount
from bank_app.application.ports.repositories.i_bank_account import (
    IBankAccountRepository,
)


class BankAccountRepository(IBankAccountRepository):
    @classmethod
    def _get_bank_account_by_id(cls, entity_id: AccountIdentity) -> BankAccountEntity:
        try:
            return BankAccountEntity.objects.get(entity_id=entity_id.uuid)
        except BankAccountEntity.DoesNotExist as ex:
            raise NotFound(f"bank account {entity_id.uuid} does not exist") from ex

    @classmethod
    def _get_bank_account_by_account_number(
        cls, account_number: UUID
    ) -> BankAccountEntity:
        try:
            return BankAccountEntity.objects.filter(
                account_number=account_number
            ).first()
        except BankAccountEntity.DoesNotExist as ex:
            raise NotFound(
                f"Bank account with number {account_number} does not exist"
            ) from ex

    @classmethod
    def _to_entity(cls, entity: BankAccount) -> BankAccountEntity:
        return BankAccountEntity(
            entity_id=entity.entity_id.uuid,
            account_number=entity.account_number,
            balance=entity.balance,
            overdraft_amount=entity.overdraft_amount,
            is_allow_overdraft=entity.is_allow_overdraft,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    @classmethod
    def _to_domain(cls, entity: BankAccountEntity) -> BankAccount:
        return BankAccount(
            entity_id=AccountIdentity(entity.entity_id),
            account_number=entity.account_number,
            balance=entity.balance,
            overdraft_amount=entity.overdraft_amount,
            is_allow_overdraft=entity.is_allow_overdraft,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    @classmethod
    def get(cls, entity_id: EntityIdentity) -> BankAccount:
        if not isinstance(entity_id, AccountIdentity):
            raise ValueError("entity_id must be an AccountIdentity")

        bank_account_entity = cls._get_bank_account_by_id(entity_id)
        return cls._to_domain(bank_account_entity)

    @classmethod
    def get_by_bank_account_number(cls, account_number: UUID) -> BankAccount:
        bank_account_entity = cls._get_bank_account_by_account_number(account_number)
        return cls._to_domain(bank_account_entity)

    @classmethod
    def delete(cls, entity_id: EntityIdentity, **kwargs: Any) -> None:
        if not isinstance(entity_id, AccountIdentity):
            raise ValueError("entity_id must be an AccountIdentity")

        bank_account_entity = cls._get_bank_account_by_id(entity_id)
        bank_account_entity.delete()

    @classmethod
    def save(cls, entity: Entity) -> None:
        if not isinstance(entity, BankAccount):
            raise ValueError("entity must be a BankAccount")
        try:
            existing_entity = cls._get_bank_account_by_id(entity_id=entity.entity_id)
            existing_entity.account_number = entity.account_number
            existing_entity.balance = entity.balance
            existing_entity.overdraft_amount = entity.overdraft_amount
            existing_entity.is_allow_overdraft = entity.is_allow_overdraft
            existing_entity.is_active = entity.is_active
            existing_entity.updated_at = entity.updated_at
            existing_entity.save()
        except BankAccountEntity.DoesNotExist:
            bank_account_entity = cls._to_entity(entity)
            bank_account_entity.save()

    @classmethod
    def update_overdraft_amount(
        cls, account_number: UUID, overdraft_amount: Decimal
    ) -> None:
        if overdraft_amount < 0:
            raise ValueError("Overdraft amount cannot be negative")
        try:
            bank_account_entity = cls._get_bank_account_by_account_number(
                account_number
            )
            bank_account_entity.overdraft_amount = overdraft_amount
            bank_account_entity.save()
        except BankAccountEntity.DoesNotExist as ex:
            raise NotFound(
                f"Bank account with number {account_number} does not exist"
            ) from ex
