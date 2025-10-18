from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

from bank_app.application.domain.exceptions import BusinessException, NotFound


def problem_response(detail: str, status_code: int) -> Response:
    return Response(
        {"detail": detail}, status=status_code, content_type="application/problem+json"
    )


def exceptions_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        return response

    if isinstance(exc, NotFound) or isinstance(exc, BusinessException):
        return problem_response(str(exc.message), status.HTTP_404_NOT_FOUND)
    return problem_response(str(exc), status.HTTP_500_INTERNAL_SERVER_ERROR)
