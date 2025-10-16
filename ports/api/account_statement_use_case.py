import datetime
from typing import Optional
from uuid import UUID

from domain.domain_models import DomainService
from domain.dtos.account_statement import MonthlyStatementDTO
from infrastructure.util import AccountType


class AccountStatementUseCase(DomainService):
    def generate_monthly_statement(
        self,
        account_id: UUID,
        type_account: AccountType = AccountType.CURRENT_ACCOUNT,
        period_end: Optional[datetime.datetime] = None,
    ) -> MonthlyStatementDTO:
        """generate a monthly report of current account or booklet account"""
        raise NotImplementedError
