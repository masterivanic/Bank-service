from uuid import uuid4

from django.db import models


class BookletAccountEntity(models.Model):
    entity_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    account_number = models.UUIDField(default=uuid4)
    balance = models.DecimalField(max_digits=19, decimal_places=2)
    deposit_limit = models.DecimalField(max_digits=19, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "booklet_account"

    def __str__(self):
        return f"Bookle account number #{self.entity_id}"
