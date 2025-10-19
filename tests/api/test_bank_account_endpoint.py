import uuid

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestBankAccountDepositView:
    api_client = APIClient()
    url = reverse("bank-account-deposit")

    def test_deposit_money_success(self, build_bank_account):
        bank_account = build_bank_account()
        data = {"account_number": bank_account.account_number, "amount": "1000.00"}
        response = self.api_client.post(self.url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert uuid.UUID(response.data["entity_id"]) == bank_account.entity_id
        assert response.data["balance"] == "2000.00"
        assert uuid.UUID(response.data["account_number"]) == bank_account.account_number

    def test_deposit_money_invalid_account_number(self):
        invalid_data = {"account_number": "invalid-uuid", "amount": "100.50"}
        response = self.api_client.post(self.url, data=invalid_data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "account_number" in response.data

    def test_deposit_money_negative_amount(self, build_bank_account):
        bank_account = build_bank_account()
        data = {"account_number": str(bank_account.account_number), "amount": "-100.50"}

        response = self.api_client.post(self.url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "amount" in response.data or "non_field_errors" in response.data

    def test_deposit_money_zero_amount(self, build_bank_account):
        bank_account = build_bank_account()
        data = {"account_number": str(bank_account.account_number), "amount": "0.00"}
        response = self.api_client.post(self.url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_deposit_money_missing_account_number(self):
        invalid_data = {"amount": "100.50"}
        response = self.api_client.post(self.url, data=invalid_data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "account_number" in response.data

    def test_deposit_money_missing_amount(self, build_bank_account):
        bank_account = build_bank_account()
        invalid_data = {"account_number": str(bank_account.account_number)}
        response = self.api_client.post(self.url, data=invalid_data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "amount" in response.data

    def test_deposit_money_large_amount(self, build_bank_account):
        bank_account = build_bank_account(zero_balance=True)
        data = {
            "account_number": str(bank_account.account_number),
            "amount": "99999999999999999.99",
        }
        response = self.api_client.post(self.url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert uuid.UUID(response.data["entity_id"]) == bank_account.entity_id
        assert response.data["balance"] == data["amount"]
        assert uuid.UUID(response.data["account_number"]) == bank_account.account_number

    def test_deposit_money_service_raises_not_found(
        self,
    ):
        data = {"account_number": str(uuid.uuid4()), "amount": "400.00"}
        response = self.api_client.post(self.url, data, format="json")
        assert response.status_code == status.HTTP_404_NOT_FOUND
