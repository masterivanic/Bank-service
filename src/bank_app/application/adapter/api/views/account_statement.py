from dependency_injector.wiring import Provide, inject
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from bank_app.application.adapter.api.serializers.account_statement import (
    AccountStatementResultSerializer,
    AccountStatementSerializer,
)
from bank_app.application.service.account_statement import (
    AccountStatementService as AccountStatementUseCase,
)
from exalt_hexarch.containers import Container


class BankAccountStatementView(APIView):
    @inject
    def post(
        self,
        request: Request,
        account_statement_service: AccountStatementUseCase = Provide[
            Container.account_statement_service
        ],
    ) -> Response:
        serializer = AccountStatementSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account_id = serializer.validated_data["account_id"]
        type_account = serializer.validated_data["type_account"]
        period_end = serializer.validated_data["period_end"]
        result = account_statement_service.generate_monthly_statement(
            account_id=account_id,
            type_account=type_account,
            period_end=period_end,
        )
        return Response(
            data=AccountStatementResultSerializer(result).data,
            status=status.HTTP_200_OK,
        )
