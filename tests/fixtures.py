from typing import Any, Callable

import pytest

from tests.factory import BankAccountModelFactory, BookletAccountModelFactory


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
