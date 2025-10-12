from decimal import Decimal

import pytest

from domain.dtos.bank_account import BankAccountDTO
from domain.exceptions import BusinessException, NotFound
from domain.model.bank_account import BankAccount


class TestBankAccountRedrawAndDepositService:
    class TestRedraw:
        def test_redraw_successful(
            self,
            bank_account_service,
            mock_bank_account_repository,
            mock_bank_account,
            sample_account_number,
            monkeypatch,
        ):
            amount = Decimal("100.00")
            mock_bank_account_repository.get_by_bank_account_number.return_value = (
                mock_bank_account
            )
            mock_bank_account_repository.save.return_value = None

            monkeypatch.setattr(
                "domain.service.bank_account.BankAccountService.can_withdraw",
                lambda account, withdrawal_amount: True,
            )
            result = bank_account_service.redraw(sample_account_number, amount)

            mock_bank_account_repository.get_by_bank_account_number.assert_called_once_with(
                acount_number=sample_account_number
            )
            mock_bank_account.withdraw.assert_called_once_with(amount=amount)
            mock_bank_account_repository.save.assert_called_once_with(mock_bank_account)

            assert isinstance(result, BankAccountDTO)
            assert result.entity_id == mock_bank_account.entity_id
            assert result.account_number == mock_bank_account.account_number
            assert result.balance == mock_bank_account.balance

        def test_redraw_account_not_found(
            self,
            bank_account_service,
            mock_bank_account_repository,
            sample_account_number,
        ):
            amount = Decimal("100.00")
            mock_bank_account_repository.get_by_bank_account_number.return_value = None

            with pytest.raises(NotFound) as ex:
                bank_account_service.redraw(sample_account_number, amount)

            assert (
                f"Account with number {sample_account_number} not found"
                == ex.value.message
            )
            mock_bank_account_repository.get_by_bank_account_number.assert_called_once_with(
                acount_number=sample_account_number
            )
            mock_bank_account_repository.save.assert_not_called()

        def test_redraw_insufficient_funds(
            self,
            bank_account_service,
            mock_bank_account_repository,
            mock_bank_account,
            sample_account_number,
            monkeypatch,
        ):
            amount = Decimal("1500.00")
            mock_bank_account_repository.get_by_bank_account_number.return_value = (
                mock_bank_account
            )

            monkeypatch.setattr(
                "domain.service.bank_account.BankAccountService.can_withdraw",
                lambda account, withdrawal_amount: False,
            )

            with pytest.raises(BusinessException) as exc_info:
                bank_account_service.redraw(sample_account_number, amount)

            assert (
                exc_info.value.message == "Insufficient funds to make this withdrawal"
            )
            mock_bank_account_repository.get_by_bank_account_number.assert_called_once_with(
                acount_number=sample_account_number
            )
            mock_bank_account.withdraw.assert_not_called()
            mock_bank_account_repository.save.assert_not_called()

        def test_redraw_zero_amount_should_fail(
            self,
            bank_account_service,
            mock_bank_account_repository,
            mock_bank_account,
            sample_account_number,
        ):
            amount = Decimal("0.00")
            mock_bank_account_repository.get_by_bank_account_number.return_value = (
                mock_bank_account
            )
            with pytest.raises(ValueError) as ex:
                bank_account_service.redraw(sample_account_number, amount)

            assert str(ex.value) == "cannot redraw null or negative amount"

        def test_redraw_negative_amount_should_fail(
            self,
            bank_account_service,
            mock_bank_account_repository,
            mock_bank_account,
            sample_account_number,
        ):
            amount = Decimal("-100.00")
            mock_bank_account_repository.get_by_bank_account_number.return_value = (
                mock_bank_account
            )
            with pytest.raises(ValueError) as ex:
                bank_account_service.redraw(sample_account_number, amount)
            assert str(ex.value) == "cannot redraw null or negative amount"

    class TestDepositMoney:
        def test_deposit_money_successful(
            self,
            bank_account_service,
            mock_bank_account_repository,
            sample_entity_id,
            sample_account_number,
        ):
            initial_balance = Decimal("1000.00")
            amount = Decimal("500.00")

            real_bank_account = BankAccount(
                entity_id=sample_entity_id,
                account_number=sample_account_number,
                balance=initial_balance,
            )
            mock_bank_account_repository.get_by_bank_account_number.return_value = (
                real_bank_account
            )
            mock_bank_account_repository.save.return_value = None

            result = bank_account_service.deposit_money(sample_account_number, amount)

            mock_bank_account_repository.get_by_bank_account_number.assert_called_once_with(
                acount_number=sample_account_number
            )
            mock_bank_account_repository.save.assert_called_once_with(real_bank_account)

            assert isinstance(result, BankAccountDTO)
            assert result.entity_id == real_bank_account.entity_id
            assert result.account_number == real_bank_account.account_number
            assert result.balance == real_bank_account.balance == Decimal("1500.00")

        def test_deposit_money_account_not_found(
            self,
            bank_account_service,
            mock_bank_account_repository,
            sample_account_number,
        ):
            amount = Decimal("500.00")
            mock_bank_account_repository.get_by_bank_account_number.return_value = None

            with pytest.raises(NotFound) as ex:
                bank_account_service.deposit_money(sample_account_number, amount)

            assert f"Account with number {sample_account_number} not found" in str(
                ex.value.message
            )

        def test_deposit_money_zero_amount_should_fail(
            self,
            bank_account_service,
            mock_bank_account_repository,
            mock_bank_account,
            sample_account_number,
        ):
            amount = Decimal("0.00")
            mock_bank_account_repository.get_by_bank_account_number.return_value = (
                mock_bank_account
            )

            with pytest.raises(ValueError) as ex:
                bank_account_service.deposit_money(sample_account_number, amount)

            assert "cannot deposit null or negative amount" in str(ex.value)

        def test_deposit_money_negative_amount_should_fail(
            self,
            bank_account_service,
            mock_bank_account_repository,
            mock_bank_account,
            sample_account_number,
        ):
            amount = Decimal("-100.00")
            mock_bank_account_repository.get_by_bank_account_number.return_value = (
                mock_bank_account
            )
            with pytest.raises(ValueError) as ex:
                bank_account_service.deposit_money(sample_account_number, amount)

            assert "cannot deposit null or negative amount" in str(ex.value)
