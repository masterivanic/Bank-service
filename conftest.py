import datetime
from decimal import Decimal
from unittest.mock import Mock, PropertyMock, create_autospec
from uuid import UUID, uuid4

import pytest

from bank_app.application.adapter.persistence.repository.bank_account_repository import (
    BankAccountRepository,
)
from bank_app.application.domain.model.bank_account import AccountIdentity, BankAccount
from bank_app.application.ports.repositories.i_bank_account import (
    IBankAccountRepository,
)
from bank_app.application.service.bank_account import BankAccountRedrawAndDepositService
from tests.fixtures import *


@pytest.fixture()
def mock_bank_account_repository():
    return create_autospec(IBankAccountRepository)


@pytest.fixture()
def bank_account_service(mock_bank_account_repository):
    return BankAccountRedrawAndDepositService(mock_bank_account_repository)


@pytest.fixture()
def bank_account_service_implement():
    return BankAccountRedrawAndDepositService(BankAccountRepository())


@pytest.fixture()
def sample_account_number():
    return UUID("7ebd50e7-0000-0000-0000-000000000000")


@pytest.fixture()
def sample_entity_id():
    return AccountIdentity(uuid4)


@pytest.fixture()
def mock_bank_account(sample_entity_id, sample_account_number):
    account = create_autospec(BankAccount)
    account.entity_id = sample_entity_id
    account.account_number = sample_account_number
    account.balance = Decimal("1000.00")
    account.withdraw = Mock()
    account.deposit = Mock()
    return account


@pytest.fixture()
def mock_bank_account_overdraft(sample_entity_id, sample_account_number):
    account = create_autospec(BankAccount)
    account.entity_id = sample_entity_id
    account.account_number = sample_account_number
    account.balance = Decimal("1000.00")
    account.overdraft_amount = Decimal("500.00")
    account.is_allow_overdraft = True
    account.is_active = True
    account.created_at = datetime.datetime.now()
    account.updated_at = datetime.datetime.now()

    def has_sufficient_funds_side_effect(amount):
        if account.is_allow_overdraft:
            available_balance = account.balance + account.overdraft_amount
            return available_balance >= amount
        return account.balance >= amount

    account.has_sufficient_funds = Mock(side_effect=has_sufficient_funds_side_effect)

    @property
    def available_balance_property(self):
        if self.is_allow_overdraft:
            return self.balance + self.overdraft_amount
        return self.balance

    available_balance_mock = PropertyMock()
    available_balance_mock.return_value = Decimal("1500.00")
    type(account).available_balance = available_balance_mock

    account.withdraw = Mock()
    account.deposit = Mock()
    account.set_overdraft_amount = Mock()
    account.is_in_overdraft = Mock(return_value=False)
    account.get_overdraft_used = Mock(return_value=Decimal("0.00"))

    return account
