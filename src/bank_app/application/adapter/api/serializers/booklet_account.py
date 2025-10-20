from decimal import Decimal

import attr
from rest_framework import serializers

from bank_app.application.adapter.persistence.entity.booklet_account_entity import (
    BookletAccountEntity,
)
from bank_app.application.domain.dtos.booklet_account import BookletAccountDTO


class BookletAccountSerializer(serializers.Serializer):
    account_number = serializers.UUIDField()
    amount = serializers.DecimalField(
        max_digits=19, decimal_places=2, min_value=Decimal("0.00")
    )

    def validate(self, attrs):
        if attrs["amount"] <= 0:
            raise serializers.ValidationError("negative or null amount is not allow")
        return super().validate(attrs)


class BookletAccountResultSerializer(serializers.Serializer):
    entity_id = serializers.UUIDField()
    account_number = serializers.UUIDField()
    balance = serializers.DecimalField(max_digits=19, decimal_places=2)
    deposit_limit = serializers.DecimalField(max_digits=19, decimal_places=2)
    is_active = serializers.BooleanField()
    remaining_deposit_capacity = serializers.DecimalField(
        max_digits=19, decimal_places=2
    )

    def to_representation(self, instance: BookletAccountDTO):
        return {k: str(v) for k, v in attr.asdict(instance).items()}


class BookletAccountCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookletAccountEntity
        fields = ["balance", "deposit_limit", "is_active"]
        read_only_fields = ["entity_id", "created_at", "updated_at", "account_number"]

    def validate_balance(self, value):
        if value < 0:
            raise serializers.ValidationError("negative or null amount is not allow")
        return value


class BookletDetailSerializer(serializers.Serializer):
    entity_id = serializers.UUIDField()
    account_number = serializers.UUIDField()
    balance = serializers.DecimalField(max_digits=19, decimal_places=2)
    deposit_limit = serializers.DecimalField(max_digits=19, decimal_places=2)
