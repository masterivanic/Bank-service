from decimal import Decimal
from unittest.mock import Mock
from uuid import uuid4

import pytest

from domain.dtos.bank_account import BankAccountDTO
from domain.exceptions import NotFound, OverdraftLimitExceededException
from domain.model.bank_account import AccountIdentity, BankAccount
from domain.service.bank_account import BankAccountService
from service.bank_acount_overdraft import BankAccountOverdraftService


class TestBankAccountOverdraftService:
    @pytest.fixture
    def mock_bank_account_service(self):
        return BankAccountService

    @pytest.fixture
    def overdraft_service(
        self, mock_bank_account_repository, mock_bank_account_service
    ):
        return BankAccountOverdraftService(
            bank_account_repository=mock_bank_account_repository,
            bank_account_service=mock_bank_account_service,
        )

    @pytest.fixture
    def sample_account_dto(self, mock_bank_account_overdraft):
        return BankAccountDTO(
            entity_id=mock_bank_account_overdraft.entity_id,
            account_number=mock_bank_account_overdraft.account_number,
            balance=mock_bank_account_overdraft.balance,
            overdraft_amount=mock_bank_account_overdraft.overdraft_amount,
        )

    def test_withdraw_from_account_success(
        self,
        overdraft_service,
        mock_bank_account_repository,
        mock_bank_account_service,
        mock_bank_account_overdraft,
    ):
        account_number = mock_bank_account_overdraft.account_number
        amount = Decimal("800.00")
        mock_bank_account_repository.get_by_bank_account_number.return_value = (
            mock_bank_account_overdraft
        )
        result = overdraft_service.withdraw_from_account(account_number, amount)
        mock_bank_account_repository.get_by_bank_account_number.assert_called_once_with(
            account_number=account_number
        )
        mock_bank_account_service.authorize_withdrawal(
            mock_bank_account_overdraft, amount
        )
        mock_bank_account_overdraft.withdraw.assert_called_once_with(amount=amount)
        mock_bank_account_repository.save.assert_called_once_with(
            mock_bank_account_overdraft
        )
        assert isinstance(result, BankAccountDTO)
        assert result.account_number == mock_bank_account_overdraft.account_number

    def test_withdraw_from_account_with_overdraft_success(
        self,
        overdraft_service,
        mock_bank_account_repository,
    ):
        account = BankAccount(
            entity_id=AccountIdentity(uuid=uuid4()),
            account_number=uuid4(),
            balance=Decimal("1000.00"),
            overdraft_amount=Decimal("500.00"),
            is_allow_overdraft=True,
        )
        account_number = account.account_number
        amount = Decimal("1400.00")

        mock_bank_account_repository.get_by_bank_account_number.return_value = account
        result = overdraft_service.withdraw_from_account(account_number, amount)

        mock_bank_account_repository.save.assert_called_once_with(account)
        assert isinstance(result, BankAccountDTO)

        expected_balance = Decimal("1000.00") - Decimal("1400.00")  # -400
        assert result.balance == expected_balance
        assert account.balance == expected_balance

    def test_withdraw_from_account_account_not_found(
        self, overdraft_service, mock_bank_account_repository
    ):
        account_number = uuid4()
        amount = Decimal("100.00")
        mock_bank_account_repository.get_by_bank_account_number.return_value = None

        with pytest.raises(NotFound) as exc_info:
            overdraft_service.withdraw_from_account(account_number, amount)

        assert f"Account with number {account_number} not found" in str(
            exc_info.value.message
        )

    def test_withdraw_from_account_zero_amount(
        self,
        overdraft_service,
        mock_bank_account_repository,
        mock_bank_account_overdraft,
    ):
        account_number = mock_bank_account_overdraft.account_number
        amount = Decimal("0.00")
        mock_bank_account_repository.get_by_bank_account_number.return_value = (
            mock_bank_account_overdraft
        )

        with pytest.raises(ValueError) as exc_info:
            overdraft_service.withdraw_from_account(account_number, amount)

        assert "cannot redraw null or negative amount" in str(exc_info.value)

    def test_withdraw_from_account_negative_amount(
        self,
        overdraft_service,
        mock_bank_account_repository,
        mock_bank_account_overdraft,
    ):
        mock_bank_account_service = Mock(spec=BankAccountService)
        overdraft_service._bank_account_service = mock_bank_account_service
        account_number = mock_bank_account_overdraft.account_number
        amount = Decimal("-100.00")
        mock_bank_account_repository.get_by_bank_account_number.return_value = (
            mock_bank_account_overdraft
        )

        with pytest.raises(ValueError) as ex:
            overdraft_service.withdraw_from_account(account_number, amount)

        assert "cannot redraw null or negative amount" in str(ex.value)

    def test_withdraw_from_account_authorization_failed(
        self,
        overdraft_service,
        mock_bank_account_repository,
        mock_bank_account_overdraft,
    ):
        mock_bank_account_service = Mock(spec=BankAccountService)
        overdraft_service._bank_account_service = mock_bank_account_service

        account_number = mock_bank_account_overdraft.account_number
        amount = Decimal("2000.00")

        mock_bank_account_repository.get_by_bank_account_number.return_value = (
            mock_bank_account_overdraft
        )

        mock_bank_account_service.authorize_withdrawal.side_effect = (
            OverdraftLimitExceededException(
                f"Withdrawal of {amount} exceeds overdraft limit."
            )
        )

        with pytest.raises(OverdraftLimitExceededException) as ex:
            overdraft_service.withdraw_from_account(account_number, amount)

        assert f"Withdrawal of {amount} exceeds overdraft limit." in str(
            ex.value.message
        )

    def test_set_overdraft_amount_success(
        self,
        overdraft_service,
        mock_bank_account_repository,
        mock_bank_account_overdraft,
    ):
        account_number = mock_bank_account_overdraft.account_number
        overdraft_amount = Decimal("1000.00")
        mock_bank_account_repository.get_by_bank_account_number.return_value = (
            mock_bank_account_overdraft
        )

        def set_overdraft_side_effect(amount):
            mock_bank_account_overdraft.overdraft_amount = amount

        mock_bank_account_overdraft.set_overdraft_amount.side_effect = (
            set_overdraft_side_effect
        )

        result = overdraft_service.set_overdraft_amount(
            account_number=account_number, overdraft_amount=overdraft_amount
        )

        mock_bank_account_repository.get_by_bank_account_number.assert_called_once_with(
            account_number
        )
        mock_bank_account_overdraft.set_overdraft_amount.assert_called_once_with(
            overdraft_amount
        )
        mock_bank_account_repository.save.assert_called_once_with(
            mock_bank_account_overdraft
        )

        assert isinstance(result, BankAccountDTO)
        assert result.overdraft_amount == overdraft_amount

    def test_set_overdraft_amount_account_not_found(
        self, overdraft_service, mock_bank_account_repository
    ):
        account_number = uuid4()
        overdraft_amount = Decimal("500.00")
        mock_bank_account_repository.get_by_bank_account_number.return_value = None

        with pytest.raises(NotFound) as exc_info:
            overdraft_service.set_overdraft_amount(account_number, overdraft_amount)

        assert f"Account with number {account_number} not found" in str(
            exc_info.value.message
        )
        mock_bank_account_repository.save.assert_not_called()

    def test_get_available_balance_success(
        self,
        overdraft_service,
        mock_bank_account_repository,
        mock_bank_account_overdraft,
    ):
        account_number = mock_bank_account_overdraft.account_number
        expected_available_balance = (
            mock_bank_account_overdraft.balance
            + mock_bank_account_overdraft.overdraft_amount
        )

        mock_bank_account_repository.get_by_bank_account_number.return_value = (
            mock_bank_account_overdraft
        )
        result = overdraft_service.get_available_balance(account_number)
        mock_bank_account_repository.get_by_bank_account_number.assert_called_once_with(
            account_number
        )
        assert result == expected_available_balance
