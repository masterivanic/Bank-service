from decimal import Decimal
from unittest.mock import Mock, create_autospec
from uuid import uuid4

import pytest

from src.domain.dtos.booklet_account import BookletAccountDTO
from src.domain.exceptions import NotFound
from src.domain.model.booklet_account import BookletAccount
from src.domain.service import booklet_account
from src.ports.repositories.i_booklet_account import IBookletAccountRepository
from src.service.booklet_account import BookletAccountService


class TestBookletAccountService:
    @pytest.fixture
    def mock_repository(self):
        return create_autospec(IBookletAccountRepository)

    @pytest.fixture
    def mock_service(self):
        return booklet_account.BookletAcountService

    @pytest.fixture
    def booklet_account_service(self, mock_repository, mock_service):
        return BookletAccountService(
            booklet_account_repository=mock_repository,
            booklet_account_service=mock_service,
        )

    @pytest.fixture
    def sample_booklet_account(self):
        account = Mock(spec=BookletAccount)
        account.withdraw = Mock()
        account.deposit = Mock()
        account.set_deposit_limit = Mock()
        account.balance = Decimal("1000.00")
        account.deposit_limit = Decimal("5000.00")
        account.has_sufficient_funds = Mock(return_value=True)
        return account

    @pytest.fixture
    def sample_account_number(self):
        return uuid4()

    @pytest.fixture
    def sample_booklet_account_dto(self):
        return Mock(spec=BookletAccountDTO)

    def test_redraw_success(
        self,
        booklet_account_service,
        mock_repository,
        mock_service,
        sample_booklet_account,
        sample_account_number,
        sample_booklet_account_dto,
    ):
        amount = Decimal("100.50")
        initial_balance = Decimal("500.00")
        expected_balance_after_withdraw = Decimal("399.50")

        sample_booklet_account.balance = initial_balance

        def withdraw_side_effect(withdraw_amount):
            sample_booklet_account.balance -= withdraw_amount

        sample_booklet_account.withdraw.side_effect = withdraw_side_effect

        mock_repository.get_by_booklet_account_number.return_value = (
            sample_booklet_account
        )
        mock_repository.save.return_value = None
        BookletAccountDTO.from_entity = Mock(return_value=sample_booklet_account_dto)

        result = booklet_account_service.redraw(sample_account_number, amount)
        mock_repository.get_by_booklet_account_number.assert_called_once_with(
            sample_account_number
        )
        mock_service.authorize_withdrawal(sample_booklet_account, amount)
        sample_booklet_account.withdraw.assert_called_once_with(amount)
        mock_repository.save.assert_called_once_with(sample_booklet_account)
        BookletAccountDTO.from_entity.assert_called_once_with(sample_booklet_account)

        assert result == sample_booklet_account_dto
        assert sample_booklet_account.balance == expected_balance_after_withdraw

    def test_redraw_account_not_found(
        self, booklet_account_service, mock_repository, sample_account_number
    ):
        amount = Decimal("100.50")
        mock_repository.get_by_booklet_account_number.return_value = None

        with pytest.raises(NotFound) as ex:
            booklet_account_service.redraw(sample_account_number, amount)
        assert f"Account with number {sample_account_number} not found" in str(
            ex.value.message
        )

    def test_redraw_negative_amount(
        self,
        booklet_account_service,
        mock_repository,
        sample_booklet_account,
        sample_account_number,
    ):
        amount = Decimal("-50.00")
        mock_repository.get_by_booklet_account_number.return_value = (
            sample_booklet_account
        )

        with pytest.raises(ValueError) as ex:
            booklet_account_service.redraw(sample_account_number, amount)

        assert "cannot redraw null or negative amount" in str(ex.value)

    def test_redraw_zero_amount(
        self,
        booklet_account_service,
        mock_repository,
        sample_booklet_account,
        sample_account_number,
    ):
        amount = Decimal("0.00")
        mock_repository.get_by_booklet_account_number.return_value = (
            sample_booklet_account
        )

        with pytest.raises(ValueError) as ex:
            booklet_account_service.redraw(sample_account_number, amount)

        assert "cannot redraw null or negative amount" in str(ex.value)
        sample_booklet_account.withdraw.assert_not_called()
        mock_repository.save.assert_not_called()

    def test_deposit_money_success(
        self,
        booklet_account_service,
        mock_repository,
        mock_service,
        sample_booklet_account,
        sample_account_number,
        sample_booklet_account_dto,
    ):
        amount = Decimal("200.75")
        initial_balance = Decimal("1000.00")
        deposit_limit = Decimal("5000.00")

        assert initial_balance + amount <= deposit_limit, (
            "Test setup: deposit would exceed limit"
        )

        balance_tracker = {"initial": initial_balance, "after_deposit": None}

        def deposit_mock(deposit_amount):
            new_balance = balance_tracker["initial"] + deposit_amount
            balance_tracker["after_deposit"] = new_balance

        sample_booklet_account.deposit.side_effect = deposit_mock
        sample_booklet_account.balance = initial_balance
        sample_booklet_account.deposit_limit = deposit_limit

        mock_repository.get_by_booklet_account_number.return_value = (
            sample_booklet_account
        )
        mock_repository.save.return_value = None
        BookletAccountDTO.from_entity = Mock(return_value=sample_booklet_account_dto)

        result = booklet_account_service.deposit_money(sample_account_number, amount)

        mock_repository.get_by_booklet_account_number.assert_called_once_with(
            sample_account_number
        )
        mock_service.authorize_deposit(sample_booklet_account, amount)
        sample_booklet_account.deposit.assert_called_once_with(amount)
        mock_repository.save.assert_called_once_with(sample_booklet_account)
        BookletAccountDTO.from_entity.assert_called_once_with(sample_booklet_account)
        assert result == sample_booklet_account_dto

        expected_final_balance = initial_balance + amount
        actual_final_balance = balance_tracker["after_deposit"]
        assert actual_final_balance == expected_final_balance

    def test_deposit_money_account_not_found(
        self, booklet_account_service, mock_repository, sample_account_number
    ):
        amount = Decimal("200.75")
        mock_repository.get_by_booklet_account_number.return_value = None

        with pytest.raises(NotFound) as ex:
            booklet_account_service.deposit_money(sample_account_number, amount)

        assert f"Account with number {sample_account_number} not found" in str(
            ex.value.message
        )
        mock_repository.get_by_booklet_account_number.assert_called_once_with(
            sample_account_number
        )
        mock_repository.save.assert_not_called()

    def test_deposit_money_negative_amount(
        self,
        booklet_account_service,
        mock_repository,
        sample_booklet_account,
        sample_account_number,
        mock_service,
    ):
        amount = Decimal("-100.00")
        mock_repository.get_by_booklet_account_number.return_value = (
            sample_booklet_account
        )

        with pytest.raises(ValueError) as ex:
            booklet_account_service.deposit_money(sample_account_number, amount)

        assert "cannot deposit null or negative amount" in str(ex.value)

        mock_repository.get_by_booklet_account_number.assert_called_once_with(
            sample_account_number
        )
        sample_booklet_account.deposit.assert_not_called()
        mock_repository.save.assert_not_called()

    def test_update_deposit_limit_success(
        self,
        booklet_account_service,
        mock_repository,
        sample_booklet_account,
        sample_account_number,
        sample_booklet_account_dto,
    ):
        old_limit = Decimal("3000.00")
        new_limit = Decimal("5000.00")
        limit_tracker = {"old_limit": old_limit, "new_limit": None}

        def set_deposit_limit_mock(limit_amount):
            limit_tracker["new_limit"] = limit_amount

        sample_booklet_account.set_deposit_limit.side_effect = set_deposit_limit_mock
        sample_booklet_account.deposit_limit = old_limit
        mock_repository.get_by_booklet_account_number.return_value = (
            sample_booklet_account
        )
        mock_repository.save.return_value = None
        BookletAccountDTO.from_entity = Mock(return_value=sample_booklet_account_dto)

        result = booklet_account_service.update_deposit_limit(
            sample_account_number, new_limit
        )

        mock_repository.get_by_booklet_account_number.assert_called_once_with(
            sample_account_number
        )
        sample_booklet_account.set_deposit_limit.assert_called_once_with(new_limit)
        mock_repository.save.assert_called_once_with(sample_booklet_account)
        BookletAccountDTO.from_entity.assert_called_once_with(sample_booklet_account)

        actual_new_limit = limit_tracker["new_limit"]
        assert result == sample_booklet_account_dto
        assert actual_new_limit == new_limit
        assert actual_new_limit > old_limit

    def test_update_deposit_limit_account_not_found(
        self, booklet_account_service, mock_repository, sample_account_number
    ):
        new_limit = Decimal("5000.00")
        mock_repository.get_by_booklet_account_number.return_value = None

        with pytest.raises(NotFound) as ex:
            booklet_account_service.update_deposit_limit(
                sample_account_number, new_limit
            )

        assert f"Account with number {sample_account_number} not found" in str(
            ex.value.message
        )
        mock_repository.get_by_booklet_account_number.assert_called_once_with(
            sample_account_number
        )
        mock_repository.save.assert_not_called()
