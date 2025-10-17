import contextlib
import datetime
from typing import TYPE_CHECKING, Optional, Union
from uuid import UUID

from bank_app.application.domain.domain_models import AccountIdentity
from bank_app.application.domain.dtos.account_statement import MonthlyStatementDTO
from bank_app.application.domain.exceptions import NotFound
from bank_app.application.domain.model.bank_account import BankAccount
from bank_app.application.domain.model.booklet_account import BookletAccount
from bank_app.application.ports.api.account_statement_use_case import (
    AccountStatementUseCase,
)
from bank_app.application.util.util import AccountType

if TYPE_CHECKING:
    from bank_app.application.domain.service.account_statement import (
        AccoutStatementService,
    )
    from bank_app.application.ports.repositories.i_account_statement import (
        IAccountStatementRepository,
    )
    from bank_app.application.ports.repositories.i_bank_account import (
        IBankAccountRepository,
    )
    from bank_app.application.ports.repositories.i_booklet_account import (
        IBookletAccountRepository,
    )
    from bank_app.application.ports.repositories.i_transaction import (
        ITransactionRepository,
    )


class AccountStatementService(AccountStatementUseCase):
    _transaction_repository: "ITransactionRepository"
    _account_statement_repository: "IAccountStatementRepository"
    _bank_account_repository: "IBankAccountRepository"
    _booklet_account_repository: "IBookletAccountRepository"
    _account_statement_service: "AccoutStatementService"

    def __init__(
        self,
        transaction_repository: "ITransactionRepository",
        account_statement_repository: "IAccountStatementRepository",
        bank_account_repository: "IBankAccountRepository",
        booklet_account_repository: "IBookletAccountRepository",
        account_statement_service: "AccoutStatementService",
    ) -> None:
        self._transaction_repository = transaction_repository
        self._account_statement_repository = account_statement_repository
        self._bank_account_repository = bank_account_repository
        self._booklet_account_repository = booklet_account_repository
        self._account_statement_service = account_statement_service

    def _get_account(
        self, account_id: UUID, type_account: AccountType = AccountType.CURRENT_ACCOUNT
    ) -> Union[BankAccount, BookletAccount, None]:
        account_identity = AccountIdentity(account_id)
        account: Union[BankAccount, BookletAccount, None] = None
        if type_account.value == "CURRENT_ACCOUNT":
            with contextlib.suppress(NotFound):
                account = self._bank_account_repository.get(entity_id=account_identity)

        if type_account.value == "BOOKLET_ACCOUNT":
            with contextlib.suppress(NotFound):
                account = self._booklet_account_repository.get(
                    entity_id=account_identity
                )
        return account

    def generate_monthly_statement(
        self,
        account_id: UUID,
        type_account: AccountType = AccountType.CURRENT_ACCOUNT,
        period_end: Optional[datetime.datetime] = None,
    ) -> MonthlyStatementDTO:
        if period_end is None:
            period_end = datetime.datetime.now()

        account = self._get_account(account_id=account_id, type_account=type_account)
        if not account:
            raise NotADirectoryError(f"Account with id {account_id} does not exist")
        transactions = self._transaction_repository.get_by_account_id(
            AccountIdentity(account_id)
        )
        account_statement = self._account_statement_service.generate_monthly_statement(
            account=account, transactions=transactions, period_end=period_end
        )
        self._account_statement_repository.save(account_statement)
        return MonthlyStatementDTO.from_entity(account_statement)
