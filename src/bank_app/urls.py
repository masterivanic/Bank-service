from django.urls import include, path
from rest_framework.routers import DefaultRouter

from bank_app.application.adapter.api.views.bank_account import (
    BankAccountDepositView,
    BankAccountManagementView,
    BankAccountRedrawView,
)
from bank_app.application.adapter.api.views.bank_account_overdraft import (
    BankAccountOverdraftRedrawView,
    BankAccountOverdraftSetAmountView,
)

router = DefaultRouter()
router.register(
    r"bank-account", BankAccountManagementView, basename="bankaccount-management"
)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "bank-account/deposit",
        BankAccountDepositView.as_view(),
        name="bank-account-deposit",
    ),
    path(
        "bank-account/redraw",
        BankAccountRedrawView.as_view(),
        name="bank-account-redraw",
    ),
    path(
        "bank-account/overdraft/redraw",
        BankAccountOverdraftRedrawView.as_view(),
        name="bank-account-overdraft-redraw",
    ),
    path(
        "bank-account/overdraft/modify",
        BankAccountOverdraftSetAmountView.as_view(),
        name="bank-account-overdraft-modify",
    ),
]
