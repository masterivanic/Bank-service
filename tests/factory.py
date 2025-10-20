from decimal import Decimal
from uuid import uuid4

import factory

from bank_app.application.adapter.persistence.entity.bank_account_entity import (
    BankAccountEntity,
)


class BankAccountModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BankAccountEntity

    entity_id = factory.LazyFunction(uuid4)
    account_number = factory.LazyFunction(uuid4)
    balance = factory.LazyAttribute(lambda _: Decimal("1000.00"))
    overdraft_amount = factory.LazyAttribute(lambda _: Decimal("500.00"))
    is_allow_overdraft = False
    is_active = True

    class Params:
        zero_balance = factory.Trait(balance=Decimal("0.00"))
        negative_balance = factory.Trait(balance=Decimal("-100.00"))
        no_overdraft = factory.Trait(
            is_allow_overdraft=False, overdraft_amount=Decimal("0.00")
        )
