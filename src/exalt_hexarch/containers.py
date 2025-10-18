from dependency_injector import containers, providers

from bank_app.application.adapter.persistence.repository.bank_account_repository import (
    BankAccountRepository,
)
from bank_app.application.service.bank_account import BankAccountRedrawAndDepositService


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    bank_account_repository = providers.Singleton(BankAccountRepository)
    bank_account_service = providers.Factory(
        BankAccountRedrawAndDepositService,
        bank_account_repository=bank_account_repository,
    )
