from uuid import uuid4

from django.db import models


class BankAccountEntity(models.Model):
    entity_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    account_number = models.UUIDField(default=uuid4)
    balance = models.DecimalField(max_digits=3, decimal_places=2)
    overdraft_amount = models.DecimalField(max_digits=3, decimal_places=2)
    is_allow_overdraft = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [["entity_id", "account_number"]]
        db_table = "bank_account"

    def __str__(self):
        return f"Bank Account Number {self.account_number}"
