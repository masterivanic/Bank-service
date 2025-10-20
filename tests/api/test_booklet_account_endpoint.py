import uuid

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestBookletDepositView:
    api_client = APIClient()
    url = reverse("booklet-account-deposit")

    def test_deposit_money_success(self, build_booklet_account):
        booklet_account = build_booklet_account(zero_balance=True)
        data = {
            "account_number": str(booklet_account.account_number),
            "amount": "100.00",
        }
        response = self.api_client.post(self.url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert uuid.UUID(response.data["entity_id"]) == booklet_account.entity_id
        assert response.data["balance"] == "100.00"
        assert (
            uuid.UUID(response.data["account_number"]) == booklet_account.account_number
        )

    def test_deposit_money_to_not_exist_account(self):
        data = {"account_number": str(uuid.uuid4()), "amount": "100.50"}
        response = self.api_client.post(self.url, data, format="json")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert (
            response.data["detail"]
            == f"Booklet account with number {data['account_number']} does not exist"
        )

    def test_deposit_money_invalid_account_number(self):
        data = {"account_number": "invalid-uuid", "amount": "100.50"}
        response = self.api_client.post(self.url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "account_number" in response.data

    def test_deposit_money_negative_amount(self, build_booklet_account):
        booklet_account = build_booklet_account()
        data = {
            "account_number": str(booklet_account.account_number),
            "amount": "-100.50",
        }
        response = self.api_client.post(self.url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_deposit_exceed_limit_allow(self, build_booklet_account):
        booklet_account = build_booklet_account()
        data = {
            "account_number": str(booklet_account.account_number),
            "amount": "7000.50",
        }
        response = self.api_client.post(self.url, data, format="json")
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data["detail"] == "Deposit would exceed deposit limit"


@pytest.mark.django_db
class TestBookletRedrawView:
    api_client = APIClient()
    url = reverse("booklet-account-redraw")

    def test_redraw_money_success(self, build_booklet_account):
        booklet_account = build_booklet_account()
        data = {
            "account_number": str(booklet_account.account_number),
            "amount": "100.00",
        }
        response = self.api_client.post(self.url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert uuid.UUID(response.data["entity_id"]) == booklet_account.entity_id
        assert response.data["balance"] == "900.00"
        assert (
            uuid.UUID(response.data["account_number"]) == booklet_account.account_number
        )

    def test_redraw_money_insufficient_funds(self, build_booklet_account):
        booklet_account = build_booklet_account()
        data = {
            "account_number": str(booklet_account.account_number),
            "amount": "2000.00",
        }
        response = self.api_client.post(self.url, data, format="json")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert (
            response.data["detail"]
            == f"Insufficient funds for withdrawal of {data['amount']}"
        )

    def test_redraw_money_account_not_found(self):
        data = {"account_number": str(uuid.uuid4()), "amount": "100.50"}
        response = self.api_client.post(self.url, data, format="json")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert (
            response.data["detail"]
            == f"Booklet account with number {data['account_number']} does not exist"
        )


@pytest.mark.django_db
class TestBookletSetDepositLimitView:
    api_client = APIClient()
    url = reverse("booklet-account-deposit-limit")

    def test_set_deposit_limit_success(self, build_booklet_account):
        booklet_account = build_booklet_account()
        data = {
            "account_number": str(booklet_account.account_number),
            "amount": "7000.00",
        }
        response = self.api_client.post(self.url, data, format="json")
        assert response.status_code == status.HTTP_200_OK

        assert uuid.UUID(response.data["entity_id"]) == booklet_account.entity_id
        assert response.data["balance"] == "1000.00"
        assert response.data["deposit_limit"] == "7000.00"
        assert (
            uuid.UUID(response.data["account_number"]) == booklet_account.account_number
        )

    def test_set_deposit_limit_negative_amount(self, build_booklet_account):
        booklet_account = build_booklet_account()
        data = {
            "account_number": str(booklet_account.account_number),
            "amount": "-700.00",
        }
        response = self.api_client.post(self.url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_set_deposit_limit_large_amount_exceed_error(self, build_booklet_account):
        booklet_account = build_booklet_account()
        data = {
            "account_number": str(booklet_account.account_number),
            "amount": "999999999999999999.99",  # Maximum based on max_digits=19, decimal_places=2
        }
        response = self.api_client.post(self.url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
