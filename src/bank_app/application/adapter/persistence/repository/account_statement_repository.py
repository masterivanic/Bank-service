from typing import Any
from uuid import UUID

from django.db import transaction

from bank_app.application.adapter.persistence.entity.account_statement_entity import (
    MonthlyStatementEntity,
    TransationEntity,
)
from bank_app.application.domain.domain_models import Entity, EntityIdentity
from bank_app.application.domain.exceptions import NotFound
from bank_app.application.domain.model.account_statement import (
    MonthlyStatement,
    MonthlyStatementIdentity,
    Transaction,
)
from bank_app.application.ports.repositories.i_account_statement import (
    IAccountStatementRepository,
)


class AccountStatementRepository(IAccountStatementRepository):
    @classmethod
    def _get_statement_by_id(
        cls, entity_id: MonthlyStatementIdentity
    ) -> MonthlyStatementEntity:
        try:
            return MonthlyStatementEntity.objects.get(entity_id=entity_id.uuid)
        except MonthlyStatementEntity.DoesNotExist as ex:
            raise NotFound(f"Monthly statement {entity_id.uuid} does not exist") from ex

    @classmethod
    def _get_transactions_for_statement(
        cls, statement_entity: MonthlyStatementEntity
    ) -> list[Transaction]:
        transaction_entities = statement_entity.transactions.all()
        transactions = []
        for trans_entity in transaction_entities:
            transaction = Transaction(
                entity_id=trans_entity.entity_id,
                account_id=trans_entity.account_id,
                transaction_type=trans_entity.transaction_type,
                amount=trans_entity.amount,
                transation_date=trans_entity.transation_date,
                balance_after=trans_entity.balance_after,
            )
            transactions.append(transaction)
        return transactions

    @classmethod
    def _to_domain(cls, entity: MonthlyStatementEntity) -> MonthlyStatement:
        transactions = cls._get_transactions_for_statement(entity)
        return MonthlyStatement(
            entity_id=MonthlyStatementIdentity(entity.entity_id),
            account_id=entity.account_id,
            account_type=entity.account_type,
            account_number=entity.account_number,
            period_start=entity.period_start,
            period_end=entity.period_end,
            generated_at=entity.generated_at,
            opening_balance=entity.opening_balance,
            closing_balance=entity.closing_balance,
            transactions=transactions,
        )

    @classmethod
    def _to_entity(cls, domain: MonthlyStatement) -> MonthlyStatementEntity:
        try:
            entity = MonthlyStatementEntity.objects.get(entity_id=domain.entity_id.uuid)
            entity.account_id = domain.account_id
            entity.account_type = domain.account_type
            entity.account_number = domain.account_number
            entity.period_start = domain.period_start
            entity.period_end = domain.period_end
            entity.opening_balance = domain.opening_balance
            entity.closing_balance = domain.closing_balance
            return entity
        except MonthlyStatementEntity.DoesNotExist:
            return MonthlyStatementEntity(
                entity_id=domain.entity_id.uuid,
                account_id=domain.account_id,
                account_type=domain.account_type,
                account_number=domain.account_number,
                period_start=domain.period_start,
                period_end=domain.period_end,
                opening_balance=domain.opening_balance,
                closing_balance=domain.closing_balance,
            )

    @classmethod
    def _link_transactions_to_statement(
        cls, statement_entity: MonthlyStatementEntity, transactions: list[Transaction]
    ) -> None:
        transaction_uuids = [t.entity_id.uuid for t in transactions]
        transaction_entities = TransationEntity.objects.filter(
            entity_id__in=transaction_uuids
        )
        statement_entity.transactions.clear()
        statement_entity.transactions.add(*transaction_entities)

    @classmethod
    def get(cls, entity_id: EntityIdentity) -> MonthlyStatement:
        if not isinstance(entity_id, MonthlyStatementIdentity):
            raise ValueError("entity_id must be an MonthlyStatementIdentity")

        statement_entity = cls._get_statement_by_id(entity_id)
        return cls._to_domain(statement_entity)

    @classmethod
    def get_by_account_number(cls, account_number: UUID) -> list[MonthlyStatement]:
        statement_entities = MonthlyStatementEntity.objects.filter(
            account_number=account_number
        ).order_by("-period_end")
        return [cls._to_domain(entity) for entity in statement_entities]

    @classmethod
    def delete(cls, entity_id: EntityIdentity, **kwargs: Any) -> None:
        if not isinstance(entity_id, MonthlyStatementIdentity):
            raise ValueError("entity_id must be an MonthlyStatementIdentity")

        statement_entity = cls._get_statement_by_id(entity_id)
        statement_entity.delete()

    @classmethod
    def save(cls, entity: Entity) -> None:
        if not isinstance(entity, MonthlyStatement):
            raise ValueError("entity must be a MonthlyStatement")

        statement_entity = cls._to_entity(entity)
        with transaction.atomic():
            statement_entity.save()
            cls._link_transactions_to_statement(statement_entity, entity.transactions)
