import datetime

from rest_framework import serializers

from bank_app.application.domain.model.account_statement import Transaction
from bank_app.application.util.util import AccountType


class AccountStatementSerializer(serializers.Serializer):
    account_id = serializers.UUIDField()
    type_account = serializers.ChoiceField(
        choices=[(acc_type.value, acc_type.name) for acc_type in AccountType],
        default=AccountType.CURRENT_ACCOUNT.value,
    )
    period_end = serializers.DateTimeField(required=False, allow_null=True)

    def validate(self, attrs):
        if "period_end" not in attrs or attrs["period_end"] is None:
            from django.utils import timezone

            attrs["period_end"] = timezone.now()
        return attrs

    def validate_type_account(self, value):
        try:
            return AccountType(value)
        except ValueError:
            raise serializers.ValidationError(
                f"Invalid account type. Must be one of: {[t.value for t in AccountType]}"
            )


class TransactionSerializer(serializers.Serializer):
    entity_id = serializers.UUIDField()
    account_id = serializers.UUIDField()
    transaction_type = serializers.CharField()
    amount = serializers.DecimalField(max_digits=19, decimal_places=2)
    transaction_date = serializers.DateTimeField()

    def to_representation(self, instance):
        if isinstance(instance, Transaction):
            return {
                "entity_id": str(instance.entity_id.uuid)
                if hasattr(instance.entity_id, "uuid")
                else str(instance.entity_id),
                "account_id": str(instance.account_id.uuid)
                if hasattr(instance.account_id, "uuid")
                else str(instance.account_id),
                "transaction_type": instance.transaction_type,
                "account_type": instance.account_type,
                "amount": str(instance.amount),
                "transaction_date": instance.transaction_date.isoformat()
                if isinstance(instance.transaction_date, datetime.datetime)
                else instance.transaction_date,
            }
        return super().to_representation(instance)


class AccountStatementResultSerializer(serializers.Serializer):
    account_id = serializers.UUIDField()
    account_type = serializers.CharField()
    account_number = serializers.UUIDField()
    generated_at = serializers.DateTimeField()
    opening_balance = serializers.DecimalField(max_digits=19, decimal_places=2)
    closing_balance = serializers.DecimalField(max_digits=19, decimal_places=2)
    transactions = TransactionSerializer(many=True)

    def to_representation(self, instance):
        if hasattr(instance, "account_id"):
            return {
                "account_id": str(instance.account_id),
                "account_type": instance.account_type,
                "account_number": str(instance.account_number),
                "generated_at": instance.generated_at.isoformat()
                if isinstance(instance.generated_at, datetime.datetime)
                else instance.generated_at,
                "opening_balance": str(instance.opening_balance),
                "closing_balance": str(instance.closing_balance),
                "transactions": TransactionSerializer(
                    instance.transactions, many=True
                ).data,
            }
        return super().to_representation(instance)
