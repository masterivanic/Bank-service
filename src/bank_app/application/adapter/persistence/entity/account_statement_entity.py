from uuid import uuid4

from django.db import models


class TransationEntity(models.Model):
    ACCOUNT_CHOICES = [
        ("CURRENT_ACCOUNT", "CURRENT_ACCOUNT"),
        ("BOOKLET_ACCOUNT", "BOOKLET_ACCOUNT"),
    ]

    entity_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    account_id = models.UUIDField()
    transaction_type = models.CharField(max_length=25, choices=ACCOUNT_CHOICES)
    amount = models.DecimalField(max_digits=3, decimal_places=2)
    transation_date = models.DateTimeField(auto_now=True)
    balance_after = models.DecimalField(max_digits=3, decimal_places=2)

    class Meta:
        db_table = "transaction"

    def __str__(self):
        return f"TransationEntity Number {self.entity_id}"


class MonthlyStatementEntity(models.Model):
    entity_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    account_id = models.UUIDField()
    account_type = models.CharField(max_length=25)
    account_number = models.UUIDField()
    period_start = models.DateTimeField()
    period_end = models.DateTimeField()
    generated_at = models.DateTimeField(auto_now=True)
    opening_balance = models.DecimalField(max_digits=3, decimal_places=2)
    closing_balance = models.DecimalField(max_digits=3, decimal_places=2)
    transactions = models.ManyToManyField(TransationEntity)

    class Meta:
        db_table = "monthlystatement"

    def __str__(self):
        return f"MonthlyStatementEntity Number {self.entity_id}"
