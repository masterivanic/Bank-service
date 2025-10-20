import datetime
from typing import Any

from bank_app.application.adapter.persistence.entity.account_statement_entity import (
    TransationEntity,
)
from bank_app.application.domain.domain_models import (
    AccountIdentity,
    Entity,
    EntityIdentity,
)
from bank_app.application.domain.exceptions import NotFound
from bank_app.application.domain.model.account_statement import (
    Transaction,
    TransactionIdentity,
)
from bank_app.application.ports.repositories.i_transaction import ITransactionRepository


class TransactionRepository(ITransactionRepository):
    @classmethod
    def _get_transaction_by_id(cls, entity_id: TransactionIdentity) -> TransationEntity:
        try:
            return TransationEntity.objects.get(entity_id=entity_id.uuid)
        except TransationEntity.DoesNotExist as ex:
            raise NotFound(f"Transaction {entity_id.uuid} does not exist") from ex

    @classmethod
    def _to_domain(cls, entity: TransationEntity) -> Transaction:
        return Transaction(
            entity_id=TransactionIdentity(entity.entity_id),
            account_id=AccountIdentity(entity.account_id),
            transaction_type=entity.transaction_type,
            account_type=entity.account_type,
            amount=entity.amount,
            transaction_date=entity.transaction_date,
        )

    @classmethod
    def _to_entity(cls, domain: Transaction) -> TransationEntity:
        try:
            entity = TransationEntity.objects.get(entity_id=domain.entity_id.uuid)
            entity.account_id = domain.account_id.uuid
            entity.transaction_type = domain.transaction_type
            entity.amount = domain.amount
            entity.transaction_date = domain.transaction_date
            entity.account_type = domain.account_type
            return entity
        except TransationEntity.DoesNotExist:
            return TransationEntity(
                entity_id=domain.entity_id.uuid,
                account_id=domain.account_id.uuid,
                transaction_type=domain.transaction_type,
                amount=domain.amount,
                transaction_date=domain.transaction_date,
                account_type=domain.account_type,
            )

    @classmethod
    def get(cls, entity_id: EntityIdentity) -> Transaction:
        if not isinstance(entity_id, TransactionIdentity):
            raise ValueError("entity_id must be an TransactionIdentity")

        transaction_entity = cls._get_transaction_by_id(entity_id)
        return cls._to_domain(transaction_entity)

    @classmethod
    def get_by_account_id(cls, account_id: AccountIdentity) -> list[Transaction]:
        transactions_entities = TransationEntity.objects.filter(
            account_id=account_id.uuid
        )
        return [cls._to_domain(entity) for entity in transactions_entities]

    @classmethod
    def get_by_account_id_and_date_range(
        cls,
        account_id: AccountIdentity,
        start_date: datetime.datetime,
        end_date: datetime.datetime,
    ) -> list[Transaction]:
        transactions_entities = TransationEntity.objects.filter(
            account_id=account_id.uuid,
            transaction_date__gte=start_date,
            transaction_date__lte=end_date,
        ).order_by("-transaction_date")
        return [cls._to_domain(entity) for entity in transactions_entities]

    @classmethod
    def delete(cls, entity_id: EntityIdentity, **kwargs: Any) -> None:
        if not isinstance(entity_id, TransactionIdentity):
            raise ValueError("entity_id must be an TransactionIdentity")

        transaction_entity = cls._get_transaction_by_id(entity_id)
        transaction_entity.delete()

    @classmethod
    def save(cls, entity: Entity) -> None:
        if not isinstance(entity, Transaction):
            raise ValueError("entity must be a Transaction")

        transaction_entity = cls._to_entity(entity)
        transaction_entity.save()
