import uuid
from decimal import Decimal

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestBankAccountOverdraftRedrawView:
    api_client = APIClient()
    url = reverse("bank-account-overdraft-redraw")

    def test_withdraw_from_account_success(self, build_bank_account):
        bank_account = build_bank_account(is_allow_overdraft=True)
        data = {"account_number": bank_account.account_number, "amount": "1400.00"}
        response = self.api_client.post(self.url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert uuid.UUID(response.data["entity_id"]) == bank_account.entity_id
        assert uuid.UUID(response.data["account_number"]) == bank_account.account_number
        assert response.data["balance"] == "-400.00"
        assert response.data["overdraft_amount"] == "500.00"

    def test_withdraw_from_account_invalid_account_number(self):
        data = {"account_number": "invalid-uuid", "amount": "100.50"}
        response = self.api_client.post(self.url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "account_number" in response.data

    def test_withdraw_from_account_negative_amount(self, build_bank_account):
        bank_account = build_bank_account(is_allow_overdraft=True)
        data = {"account_number": str(bank_account.account_number), "amount": "-100.50"}
        response = self.api_client.post(self.url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_withdraw_from_account_zero_amount(self, build_bank_account):
        bank_account = build_bank_account(is_allow_overdraft=True)
        data = {"account_number": str(bank_account.account_number), "amount": "0.00"}
        response = self.api_client.post(self.url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_withdraw_from_account_missing_fields(self):
        response1 = self.api_client.post(
            self.url, data={"amount": "100.50"}, format="json"
        )
        assert response1.status_code == status.HTTP_400_BAD_REQUEST
        assert "account_number" in response1.data

        response2 = self.api_client.post(
            self.url, data={"account_number": str(uuid.uuid4())}, format="json"
        )
        assert response2.status_code == status.HTTP_400_BAD_REQUEST
        assert "amount" in response2.data

    def test_withdraw_from_account_service_raises_not_found(self):
        data = {"account_number": str(uuid.uuid4()), "amount": "100.00"}
        response = self.api_client.post(self.url, data, format="json")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_withdraw_from_account_exceed_funds_error(
        self,
        build_bank_account,
    ):
        bank_account = build_bank_account(
            is_allow_overdraft=True, overdraft_amount=Decimal("800.00")
        )
        data = {
            "account_number": str(bank_account.account_number),
            "amount": "20000.00",
        }
        response = self.api_client.post(self.url, data, format="json")
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert (
            response.data["detail"]
            == f"Withdrawal of {data['amount']} exceeds overdraft limit."
        )

    def test_withdraw_from_account_service_raises_business_exception(
        self, build_bank_account
    ):
        bank_account = build_bank_account(
            is_allow_overdraft=False, overdraft_amount=Decimal("800.00")
        )
        data = {"account_number": str(bank_account.account_number), "amount": "1700.00"}
        response = self.api_client.post(self.url, data, format="json")
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data["detail"] == "You are not allow to overdraft"


@pytest.mark.django_db
class TestBankAccountOverdraftSetAmountView:
    api_client = APIClient()
    url = reverse("bank-account-overdraft-modify")

    def test_set_overdraft_amount_success(self, build_bank_account):
        bank_account = build_bank_account(
            is_allow_overdraft=True, overdraft_amount=Decimal("800.00")
        )
        data = {"account_number": str(bank_account.account_number), "amount": "1700.00"}
        response = self.api_client.post(self.url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert uuid.UUID(response.data["entity_id"]) == bank_account.entity_id
        assert uuid.UUID(response.data["account_number"]) == bank_account.account_number
        assert response.data["overdraft_amount"] == "1700.00"

    def test_set_overdraft_amount_invalid_account_number(self):
        data = {"account_number": "invalid-uuid", "amount": "500.00"}
        response = self.api_client.post(self.url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "account_number" in response.data

    def test_set_overdraft_amount_negative_amount(self, build_bank_account):
        bank_account = build_bank_account(is_allow_overdraft=True)
        data = {"account_number": str(bank_account.account_number), "amount": "-500.00"}
        response = self.api_client.post(self.url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
