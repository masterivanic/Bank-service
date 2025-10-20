from typing import Any, Callable

import pytest

from tests.factory import (
    BankAccountModelFactory,
    BookletAccountModelFactory,
    TransationModelFactory,
)


@pytest.fixture()
def build_bank_account() -> Callable[[dict[str, Any]], BankAccountModelFactory]:
    def _build_bank_account(save_factory=True, **kwargs):
        if save_factory:
            return BankAccountModelFactory(**kwargs)
        return BankAccountModelFactory.build(**kwargs)

    return _build_bank_account


@pytest.fixture()
def build_booklet_account() -> Callable[[dict[str, Any]], BookletAccountModelFactory]:
    def _build_booklet_account(save_factory=True, **kwargs):
        if save_factory:
            return BookletAccountModelFactory(**kwargs)
        return BookletAccountModelFactory.build(**kwargs)

    return _build_booklet_account


@pytest.fixture()
def build_transaction() -> Callable[[dict[str, Any]], TransationModelFactory]:
    def _build_transaction(
        save_factory=True, bank_account=None, booklet_account=None, **kwargs
    ):
        if bank_account is not None:
            kwargs["account_id"] = bank_account.entity_id
            kwargs["account_type"] = "CURRENT_ACCOUNT"

        elif booklet_account is not None:
            kwargs["account_id"] = booklet_account.entity_id
            kwargs["account_type"] = "BOOKLET_ACCOUNT"

        if save_factory:
            return TransationModelFactory(**kwargs)
        return TransationModelFactory.build(**kwargs)

    return _build_transaction
