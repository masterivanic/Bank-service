from decimal import Decimal

import pytest

from domain.exceptions import BusinessException
from domain.model.bank_account import BankAccount


class TestIntegrationScenarios:
    def test_deposit_then_redraw_balance_calculation(
        self,
        bank_account_service,
        mock_bank_account_repository,
        sample_entity_id,
        sample_account_number,
        monkeypatch,
    ):
        """
        Deposit money then withdraw money and verify balance calculations
        """
        initial_balance = Decimal("1000.00")
        deposit_amount = Decimal("500.00")
        withdraw_amount = Decimal("300.00")

        real_bank_account = BankAccount(
            entity_id=sample_entity_id,
            account_number=sample_account_number,
            balance=initial_balance,
        )

        mock_bank_account_repository.get_by_bank_account_number.return_value = (
            real_bank_account
        )
        mock_bank_account_repository.save.return_value = None

        monkeypatch.setattr(
            "domain.service.bank_account.BankAccountService.can_withdraw",
            lambda account, withdrawal_amount: True,
        )
        deposit_result = bank_account_service.deposit_money(
            sample_account_number, deposit_amount
        )

        assert deposit_result.balance == Decimal("1500.00")

        mock_bank_account_repository.get_by_bank_account_number.return_value = (
            real_bank_account
        )

        withdraw_result = bank_account_service.redraw(
            sample_account_number, withdraw_amount
        )
        assert withdraw_result.balance == Decimal("1200.00")  # 1500 - 300

        assert mock_bank_account_repository.get_by_bank_account_number.call_count == 2
        assert mock_bank_account_repository.save.call_count == 2

        mock_calls = (
            mock_bank_account_repository.get_by_bank_account_number.call_args_list
        )
        assert mock_calls[0] == mock_calls[1]

        save_calls = mock_bank_account_repository.save.call_args_list
        assert len(save_calls) == 2
        assert save_calls[0][0][0] == real_bank_account  # First save
        assert save_calls[1][0][0] == real_bank_account  # Second save

    def test_multiple_deposits_and_withdrawals_sequence(
        self,
        bank_account_service,
        mock_bank_account_repository,
        sample_entity_id,
        sample_account_number,
        monkeypatch,
    ):
        """
        Integration test: Multiple deposits and withdrawals in sequence
        """
        initial_balance = Decimal("2000.00")
        real_bank_account = BankAccount(
            entity_id=sample_entity_id,
            account_number=sample_account_number,
            balance=initial_balance,
        )

        mock_bank_account_repository.get_by_bank_account_number.return_value = (
            real_bank_account
        )
        mock_bank_account_repository.save.return_value = None

        monkeypatch.setattr(
            "domain.service.bank_account.BankAccountService.can_withdraw",
            lambda account, withdrawal_amount: True,
        )

        operations = [
            ("deposit", Decimal("1000.00"), Decimal("3000.00")),  # 2000 + 1000 = 3000
            ("withdraw", Decimal("500.00"), Decimal("2500.00")),  # 3000 - 500 = 2500
            ("deposit", Decimal("200.00"), Decimal("2700.00")),  # 2500 + 200 = 2700
            ("withdraw", Decimal("700.00"), Decimal("2000.00")),  # 2700 - 700 = 2000
        ]
        final_balance = initial_balance

        for operation_type, amount, expected_balance in operations:
            if operation_type == "deposit":
                result = bank_account_service.deposit_money(
                    sample_account_number, amount
                )
            else:
                result = bank_account_service.redraw(sample_account_number, amount)

            assert result.balance == expected_balance
            final_balance = result.balance

            mock_bank_account_repository.get_by_bank_account_number.return_value = (
                real_bank_account
            )

        assert final_balance == Decimal("2000.00")
        assert (
            mock_bank_account_repository.get_by_bank_account_number.call_count
            == len(operations)
        )
        assert mock_bank_account_repository.save.call_count == len(operations)

    def test_insufficient_funds_after_operations(
        self,
        bank_account_service,
        mock_bank_account_repository,
        sample_entity_id,
        sample_account_number,
        monkeypatch,
    ):
        """
        Verify BusinessException is raised when trying to withdraw
        more than available balance after a series of operations
        """
        initial_balance = Decimal("1000.00")
        real_bank_account = BankAccount(
            entity_id=sample_entity_id,
            account_number=sample_account_number,
            balance=initial_balance,
        )

        mock_bank_account_repository.get_by_bank_account_number.return_value = (
            real_bank_account
        )
        mock_bank_account_repository.save.return_value = None

        def really_can_withdraw_mock(account, withdrawal_amount):
            return account.balance >= withdrawal_amount

        monkeypatch.setattr(
            "domain.service.bank_account.BankAccountService.can_withdraw",
            really_can_withdraw_mock,
        )
        deposit_result = bank_account_service.deposit_money(
            sample_account_number, Decimal("200.00")
        )
        assert deposit_result.balance == Decimal("1200.00")

        mock_bank_account_repository.get_by_bank_account_number.return_value = (
            real_bank_account
        )

        withdraw_result = bank_account_service.redraw(
            sample_account_number, Decimal("800.00")
        )
        assert withdraw_result.balance == Decimal("400.00")
        mock_bank_account_repository.get_by_bank_account_number.return_value = (
            real_bank_account
        )

        with pytest.raises(BusinessException) as exc_info:
            bank_account_service.redraw(sample_account_number, Decimal("500.00"))

        assert "Insufficient funds to make this withdrawal" in str(
            exc_info.value.message
        )
        assert real_bank_account.balance == Decimal("400.00")
