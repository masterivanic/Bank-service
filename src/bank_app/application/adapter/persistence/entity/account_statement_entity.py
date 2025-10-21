from uuid import uuid4

from django.db import models


class TransactionEntity(models.Model):
    ACCOUNT_CHOICES = [
        ("CURRENT_ACCOUNT", "CURRENT_ACCOUNT"),
        ("BOOKLET_ACCOUNT", "BOOKLET_ACCOUNT"),
    ]

    TRANSACTION_TYPES = [
        ("WITHDRAWAL", "WITHDRAWAL"),
        ("DEPOSIT", "DEPOSIT"),
        ("TRANSFER", "TRANSFER"),
    ]

    entity_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    account_id = models.UUIDField()
    account_type = models.CharField(
        max_length=25, choices=ACCOUNT_CHOICES, default="CURRENT_ACCOUNT"
    )
    transaction_type = models.CharField(max_length=25, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "transaction"

    def __str__(self):
        return f"TransactionEntity Number {self.entity_id}"


class MonthlyStatementEntity(models.Model):
    entity_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    account_id = models.UUIDField()
    account_type = models.CharField(max_length=25)
    account_number = models.UUIDField()
    period_start = models.DateTimeField()
    period_end = models.DateTimeField()
    generated_at = models.DateTimeField(auto_now=True)
    opening_balance = models.DecimalField(max_digits=19, decimal_places=2)
    closing_balance = models.DecimalField(max_digits=19, decimal_places=2)
    transactions = models.ManyToManyField(TransactionEntity)

    class Meta:
        db_table = "monthlystatement"

    def __str__(self):
        return f"MonthlyStatementEntity Number {self.entity_id}"
