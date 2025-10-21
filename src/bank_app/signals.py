import logging
from uuid import uuid4

from django.db import transaction
from django.dispatch import Signal, receiver

from bank_app.application.adapter.persistence.entity.account_statement_entity import (
    TransactionEntity,
)

logger = logging.getLogger(__name__)

transaction_occurred = Signal()


@receiver(transaction_occurred)
def save_transaction_on_operation(sender, **kwargs):
    account_id = kwargs.get("account_id")
    operation_type = kwargs.get("operation_type")
    account_type = kwargs.get("account_type")  # 'DEPOSIT' or 'WITHDRAWAL'
    amount = kwargs.get("amount")

    try:
        with transaction.atomic():
            TransactionEntity.objects.create(
                entity_id=uuid4(),
                account_id=account_id,
                transaction_type=operation_type,
                account_type=account_type,
                amount=amount,
            )
            logger.info(
                f"Successfully recorded {operation_type} transaction for account {account_id}"
            )
    except Exception as ex:
        logger.error(f"Failed to save transaction record: {ex}", exc_info=True)
