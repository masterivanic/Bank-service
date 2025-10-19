from typing import Any, Callable

import pytest

from tests.factory import BankAccountModelFactory


@pytest.fixture()
def build_bank_account() -> Callable[[dict[str, Any]], BankAccountModelFactory]:
    def _build_bank_account(save_factory=True, **kwargs):
        if save_factory:
            return BankAccountModelFactory(**kwargs)
        return BankAccountModelFactory.build(**kwargs)

    return _build_bank_account
