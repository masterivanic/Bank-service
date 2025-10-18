from decimal import Decimal

import attr
from rest_framework import serializers

from bank_app.application.adapter.persistence.entity.bank_account_entity import (
    BankAccountEntity,
)
from bank_app.application.domain.dtos.bank_account import BankAccountDTO


class BankAccountSerializer(serializers.Serializer):
    account_number = serializers.UUIDField()
    amount = serializers.DecimalField(
        max_digits=19, decimal_places=2, min_value=Decimal("0.00")
    )

    def validate(self, attrs):
        if attrs["amount"] <= 0:
            raise serializers.ValidationError("negative or null amount is not allow")
        return super().validate(attrs)


class BankAccountResultSerializer(serializers.Serializer):
    entity_id = serializers.UUIDField()
    account_number = serializers.UUIDField()
    balance = serializers.DecimalField(max_digits=19, decimal_places=2)
    overdraft_amount = serializers.DecimalField(max_digits=19, decimal_places=2)

    def to_representation(self, instance: BankAccountDTO):
        return {k: str(v) for k, v in attr.asdict(instance).items()}


class BankAccountDetailSerializer(serializers.Serializer):
    entity_id = serializers.UUIDField()
    account_number = serializers.UUIDField()
    balance = serializers.DecimalField(max_digits=19, decimal_places=2)
    overdraft_amount = serializers.DecimalField(max_digits=19, decimal_places=2)


class BankAccountCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccountEntity
        fields = ["balance", "overdraft_amount", "is_allow_overdraft"]
        read_only_fields = ["entity_id", "created_at", "updated_at", "account_number"]

    def validate_balance(self, value):
        if value < 0:
            raise serializers.ValidationError("negative or null amount is not allow")
        return value
