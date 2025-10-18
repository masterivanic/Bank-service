from django.urls import include, path
from rest_framework.routers import DefaultRouter

from bank_app.application.adapter.api.views.bank_account import (
    BankAccountDepositView,
    BankAccountManagementView,
    BankAccountRedrawView,
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
        name="bank-account-deposit",
    ),
]
