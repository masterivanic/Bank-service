import datetime
import uuid
from decimal import Decimal
from typing import Union

from domain.domain_models import DomainService
from domain.model.account_statement import (
    AccountType,
    MonthlyStatement,
    MonthlyStatementIdentity,
    Transaction,
)
from domain.model.bank_account import BankAccount
from domain.model.booklet_account import BookletAccount


class AccoutStatementService(DomainService):
    @classmethod
    def generate_monthly_statement(
        cls,
        account: Union[BankAccount, BookletAccount],
        transactions: list[Transaction],
        period_end: datetime.datetime,
    ) -> "MonthlyStatement":
        period_start = period_end - datetime.timedelta(days=30)
        period_transactions = [
            t for t in transactions if period_start <= t.transation_date <= period_end
        ]
        period_transactions.sort(key=lambda x: x.transation_date, reverse=True)
        account_type = (
            AccountType.CURRENT_ACCOUNT
            if isinstance(account, BankAccount)
            else AccountType.BOOKLET_ACCOUNT
        )
        opening_balance = cls._calculate_opening_balance(
            account, transactions, period_start
        )
        return MonthlyStatement(
            entity_id=MonthlyStatementIdentity(uuid.uuid4()),
            account_id=account.entity_id.uuid,
            account_type=account_type,
            account_number=account.account_number,
            period_start=period_start,
            period_end=period_end,
            generated_at=datetime.datetime.now(),
            opening_balance=opening_balance,
            closing_balance=account.balance,
            transactions=period_transactions,
        )

    @classmethod
    def _calculate_opening_balance(
        cls,
        account: Union[BankAccount, BookletAccount],
        transactions: list[Transaction],
        period_start: datetime.datetime,
    ) -> Decimal:
        """Calculate balance at the start of the period"""
        previous_transactions = [
            t for t in transactions if t.transation_date < period_start
        ]
        previous_transactions.sort(key=lambda x: x.transation_date)

        current_balance = account.balance

        for transaction in reversed(previous_transactions):
            if transaction.transaction_type == "DEPOSIT":
                current_balance -= transaction.amount
            elif transaction.transaction_type == "WITHDRAWAL":
                current_balance += transaction.amount

        return current_balance
