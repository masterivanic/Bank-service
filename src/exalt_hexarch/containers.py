from dependency_injector import containers, providers

from bank_app.application.adapter.persistence.repository.bank_account_repository import (
    BankAccountRepository,
)
from bank_app.application.domain.service.bank_account import BankAccountService
from bank_app.application.service.bank_account import BankAccountRedrawAndDepositService
from bank_app.application.service.bank_acount_overdraft import (
    BankAccountOverdraftService,
)


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    bank_account_repository = providers.Singleton(BankAccountRepository)
    bank_account_service = providers.Factory(
        BankAccountRedrawAndDepositService,
        bank_account_repository=bank_account_repository,
    )

    bank_account_domain_service = providers.Singleton(BankAccountService)
    bank_account_overdraft_service = providers.Factory(
        BankAccountOverdraftService,
        bank_account_repository=bank_account_repository,
        bank_account_service=bank_account_domain_service,
    )
