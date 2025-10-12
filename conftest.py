from decimal import Decimal
from unittest.mock import Mock, create_autospec
from uuid import UUID, uuid4

import pytest

from application.bank_account import BankAccountRedrawAndDepositService
from domain.model.bank_account import BankAccount, BankAccountIdentity
from ports.repositories.i_bank_account import IBankAccountRepository


@pytest.fixture()
def mock_bank_account_repository():
    return create_autospec(IBankAccountRepository)


@pytest.fixture()
def bank_account_service(mock_bank_account_repository):
    return BankAccountRedrawAndDepositService(mock_bank_account_repository)


@pytest.fixture()
def sample_account_number():
    return UUID("7ebd50e7-0000-0000-0000-000000000000")


@pytest.fixture()
def sample_entity_id():
    return BankAccountIdentity(uuid4)


@pytest.fixture()
def mock_bank_account(sample_entity_id, sample_account_number):
    account = create_autospec(BankAccount)
    account.entity_id = sample_entity_id
    account.account_number = sample_account_number
    account.balance = Decimal("1000.00")
    account.withdraw = Mock()
    account.deposit = Mock()
    return account
