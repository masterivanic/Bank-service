from dependency_injector.wiring import Provide, inject
from rest_framework import status
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from bank_app.application.adapter.api.serializers.booklet_account import (
    BookletAccountCreateSerializer,
    BookletAccountResultSerializer,
    BookletAccountSerializer,
    BookletDetailSerializer,
)
from bank_app.application.adapter.persistence.entity.booklet_account_entity import (
    BookletAccountEntity,
)
from bank_app.application.service.booklet_account import (
    BookletAccountService as BookletAccountUseCase,
)
from exalt_hexarch.containers import Container


class BookletDepositView(APIView):
    @inject
    def post(
        self,
        request: Request,
        booklet_account_service: BookletAccountUseCase = Provide[
            Container.booklet_account_service
        ],
    ) -> Response:
        serializer = BookletAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account_number = serializer.validated_data["account_number"]
        amount = serializer.validated_data["amount"]
        result = booklet_account_service.deposit_money(
            account_number=account_number, amount=amount
        )
        return Response(
            data=BookletAccountResultSerializer(result).data, status=status.HTTP_200_OK
        )


class BookletRedrawView(APIView):
    @inject
    def post(
        self,
        request: Request,
        booklet_account_service: BookletAccountUseCase = Provide[
            Container.booklet_account_service
        ],
    ) -> Response:
        serializer = BookletAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account_number = serializer.validated_data["account_number"]
        amount = serializer.validated_data["amount"]
        result = booklet_account_service.redraw(
            account_number=account_number, amount=amount
        )
        return Response(
            data=BookletAccountResultSerializer(result).data, status=status.HTTP_200_OK
        )


class BookletSetDepositLimitView(APIView):
    @inject
    def post(
        self,
        request: Request,
        booklet_account_service: BookletAccountUseCase = Provide[
            Container.booklet_account_service
        ],
    ) -> Response:
        serializer = BookletAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account_number = serializer.validated_data["account_number"]
        amount = serializer.validated_data["amount"]
        result = booklet_account_service.update_deposit_limit(
            account_number=account_number, amount=amount
        )
        return Response(
            data=BookletAccountResultSerializer(result).data, status=status.HTTP_200_OK
        )


class BookletAccountManagementView(
    CreateModelMixin, RetrieveModelMixin, ListModelMixin, GenericViewSet
):
    queryset = BookletAccountEntity.objects.all()
    serializer_class = BookletAccountCreateSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return BookletAccountCreateSerializer
        return BookletDetailSerializer
