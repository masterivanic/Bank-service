from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

from src.domain.dtos.booklet_account import BookletAccountDTO
from src.domain.exceptions import NotFound
from src.ports.api.booklet_account_use_case import BookletAccount

if TYPE_CHECKING:
    from src.domain.service.booklet_account import BookletAcountService
    from src.ports.repositories.i_booklet_account import IBookletAccountRepository


class BookletAccountService(BookletAccount):
    _booklet_account_repository: "IBookletAccountRepository"
    _booklet_account_service: "BookletAcountService"

    def __init__(
        self,
        booklet_account_repository: "IBookletAccountRepository",
        booklet_account_service: "BookletAcountService",
    ) -> None:
        self._booklet_account_repository = booklet_account_repository
        self._booklet_account_service = booklet_account_service

    def redraw(self, account_number: UUID, amount: Decimal) -> BookletAccountDTO:
        booklet_account = (
            self._booklet_account_repository.get_by_booklet_account_number(
                account_number
            )
        )
        if not booklet_account:
            raise NotFound(f"Account with number {account_number} not found")

        if amount <= 0:
            raise ValueError("cannot redraw null or negative amount")
        self._booklet_account_service.authorize_withdrawal(
            account=booklet_account, amount=amount
        )
        booklet_account.withdraw(amount)
        self._booklet_account_repository.save(booklet_account)
        return BookletAccountDTO.from_entity(booklet_account)

    def deposit_money(self, account_number: UUID, amount: Decimal) -> BookletAccountDTO:
        booklet_account = (
            self._booklet_account_repository.get_by_booklet_account_number(
                account_number
            )
        )

        if not booklet_account:
            raise NotFound(f"Account with number {account_number} not found")

        if amount <= 0:
            raise ValueError("cannot deposit null or negative amount")
        self._booklet_account_service.authorize_deposit(
            account=booklet_account, amount=amount
        )
        booklet_account.deposit(amount)
        self._booklet_account_repository.save(booklet_account)
        return BookletAccountDTO.from_entity(booklet_account)

    def update_deposit_limit(
        self, account_number: UUID, amount: Decimal
    ) -> BookletAccountDTO:
        booklet_account = (
            self._booklet_account_repository.get_by_booklet_account_number(
                account_number
            )
        )

        if not booklet_account:
            raise NotFound(f"Account with number {account_number} not found")
        booklet_account.set_deposit_limit(amount)
        self._booklet_account_repository.save(booklet_account)
        return BookletAccountDTO.from_entity(booklet_account)
