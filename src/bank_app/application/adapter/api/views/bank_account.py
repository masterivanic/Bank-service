from dependency_injector.wiring import Provide, inject
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from bank_app.application.adapter.api.serializers.bank_account import (
    BankAccountCreateSerializer,
    BankAccountDetailSerializer,
    BankAccountResultSerializer,
    BankAccountSerializer,
)
from bank_app.application.adapter.persistence.entity.bank_account_entity import (
    BankAccountEntity,
)
from bank_app.application.ports.api.bank_account_use_case import (
    BankAccount as BankAccountUseCase,
)
from bank_app.signals import transaction_occurred
from exalt_hexarch.containers import Container


class BankAccountDepositView(APIView):
    @inject
    def post(
        self,
        request: Request,
        bank_account_service: BankAccountUseCase = Provide[
            Container.bank_account_service
        ],
    ) -> Response:
        serializer = BankAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account_number = serializer.validated_data["account_number"]
        amount = serializer.validated_data["amount"]
        result = bank_account_service.deposit_money(
            account_number=account_number, amount=amount
        )
        data = BankAccountResultSerializer(result).data
        transaction_occurred.send(
            sender=self.__class__,
            operation_type="DEPOSIT",
            account_id=data.get("entity_id"),
            account_type="CURRENT_ACCOUNT",
            amount=amount,
        )
        return Response(data, status=status.HTTP_200_OK)


class BankAccountRedrawView(APIView):
    @inject
    def post(
        self,
        request: Request,
        bank_account_service: BankAccountUseCase = Provide[
            Container.bank_account_service
        ],
    ) -> Response:
        serializer = BankAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account_number = serializer.validated_data["account_number"]
        amount = serializer.validated_data["amount"]
        result = bank_account_service.redraw(
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


class BankAccountManagementView(
    CreateModelMixin, RetrieveModelMixin, ListModelMixin, GenericViewSet
):
    queryset = BankAccountEntity.objects.all()
    serializer_class = BankAccountCreateSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return BankAccountCreateSerializer
        return BankAccountDetailSerializer

    @action(detail=True, methods=["post"], url_path="activate")
    def activate_account(self, request, pk=None):
        account = self.get_object()
        account.is_active = True
        account.save()
        return Response({"status": "Account activated"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="deactivate")
    def deactivate_account(self, request, pk=None):
        account = self.get_object()
        account.is_active = False
        account.save()
        return Response({"status": "Account deactivated"}, status=status.HTTP_200_OK)
