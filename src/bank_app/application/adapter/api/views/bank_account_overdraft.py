from dependency_injector.wiring import Provide, inject
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from bank_app.application.adapter.api.serializers.bank_account import (
    BankAccountResultSerializer,
    BankAccountSerializer,
)
from bank_app.application.service.bank_acount_overdraft import (
    BankAccountOverdraftService as BankAccountOverdraftUseCase,
)
from bank_app.signals import transaction_occurred
from exalt_hexarch.containers import Container


class BankAccountOverdraftRedrawView(APIView):
    @inject
    def post(
        self,
        request: Request,
        bank_account_overdraft_service: BankAccountOverdraftUseCase = Provide[
            Container.bank_account_overdraft_service
        ],
    ) -> Response:
        serializer = BankAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account_number = serializer.validated_data["account_number"]
        amount = serializer.validated_data["amount"]
        result = bank_account_overdraft_service.withdraw_from_account(
            account_number=account_number, amount=amount
        )
        data = BankAccountResultSerializer(result).data
        transaction_occurred.send(
            sender=self.__class__,
            operation_type="WITHDRAWAL",
            account_id=data.get("entity_id"),
            account_type="CURRENT_ACCOUNT",
            amount=amount,
        )
        return Response(data, status=status.HTTP_200_OK)


class BankAccountOverdraftSetAmountView(APIView):
    @inject
    def post(
        self,
        request: Request,
        bank_account_overdraft_service: BankAccountOverdraftUseCase = Provide[
            Container.bank_account_overdraft_service
        ],
    ) -> Response:
        serializer = BankAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account_number = serializer.validated_data["account_number"]
        amount = serializer.validated_data["amount"]
        result = bank_account_overdraft_service.set_overdraft_amount(
            account_number=account_number, overdraft_amount=amount
        )
        return Response(
            data=BankAccountResultSerializer(result).data, status=status.HTTP_200_OK
        )
