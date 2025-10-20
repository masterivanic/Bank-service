from decimal import Decimal
from uuid import uuid4

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestBankAccountStatementView:
    api_client = APIClient()
    url = reverse("account-statement")

    def test_generate_statement_bank_account_success(
        self, build_bank_account, build_transaction
    ):
        bank_account = build_bank_account()
        build_transaction(
            bank_account=bank_account, amount=Decimal("1000.00"), deposit=True
        )
        data = {"account_id": bank_account.entity_id, "type_account": "CURRENT_ACCOUNT"}
        response = self.api_client.post(self.url, data, format="json")

        assert response.status_code == status.HTTP_200_OK

        assert response.data["account_id"] == str(data["account_id"])
        assert response.data["account_type"] == str(data["type_account"])
        assert response.data["account_number"] == str(bank_account.account_number)
        assert response.data["transactions"][0]["account_id"] == str(
            bank_account.entity_id
        )
        assert response.data["transactions"][0]["transaction_type"] == "DEPOSIT"
        assert response.data["transactions"][0]["account_type"] == "CURRENT_ACCOUNT"
        assert len(response.data["transactions"]) == 1

    def test_generate_statement_bank_account_success(
        self, build_booklet_account, build_transaction
    ):
        booklet_account = build_booklet_account()
        build_transaction(
            booklet_account=booklet_account, amount=Decimal("1000.00"), deposit=True
        )
        data = {
            "account_id": booklet_account.entity_id,
            "type_account": "BOOKLET_ACCOUNT",
            "period_end": "2025-12-31T23:59:59Z",
        }
        response = self.api_client.post(self.url, data, format="json")

        assert response.status_code == status.HTTP_200_OK

        assert response.data["account_id"] == str(data["account_id"])
        assert response.data["account_type"] == str(data["type_account"])
        assert response.data["account_number"] == str(booklet_account.account_number)
        assert len(response.data["transactions"]) == 0

    def test_generate_statement_invalid_account_id(self):
        data = {"account_id": "invalid-uuid", "type_account": "CURRENT_ACCOUNT"}
        response = self.api_client.post(self.url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_generate_statement_missing_account_id(self):
        data = {"type_account": "CURRENT_ACCOUNT"}
        response = self.api_client.post(self.url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "account_id" in response.data

    def test_generate_statement_account_not_found(self):
        data = {"account_id": str(uuid4()), "type_account": "CURRENT_ACCOUNT"}
        response = self.api_client.post(self.url, data, format="json")
        assert response.status_code == status.HTTP_404_NOT_FOUND
