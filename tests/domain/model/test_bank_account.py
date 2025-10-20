from decimal import Decimal
from uuid import UUID

import pytest

from bank_app.application.domain.model.bank_account import AccountIdentity, BankAccount


@pytest.fixture(scope="module")
def bank_account_identify():
    return AccountIdentity(UUID("4df32c92-0000-0000-0000-000000000000"))


@pytest.fixture(scope="module")
def create_bank_account(bank_account_identify):
    return BankAccount(
        entity_id=bank_account_identify,
        account_number=UUID("7ebd50e7-0000-0000-0000-000000000000"),
        balance=Decimal(0),
    )


def test_init_bank_account(create_bank_account):
    bank_account = create_bank_account
    assert bank_account.balance == 0
    assert bank_account.account_number == UUID("7ebd50e7-0000-0000-0000-000000000000")
    assert isinstance(bank_account.entity_id, AccountIdentity)


def test_bank_account_cannot_be_create_with_negative_balance(bank_account_identify):
    with pytest.raises(ValueError) as ex:
        BankAccount(
            entity_id=bank_account_identify,
            account_number=UUID("7ebd50e7-0000-0000-0000-000000000000"),
            balance=Decimal(-100),
            is_allow_overdraft=False,
        )
    assert str(ex.value) == "The balance cannot be negative"
