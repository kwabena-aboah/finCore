from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from . models import Transaction, Budget, Payment, Asset

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'user', 'amount', 'category', 'description', 'date']
        read_only_fields = ['id', 'user', 'date']

    def validate_amount(self, value):
        if value <= 0:
            raise ValidationError("Amount must be greater than zero.")
        return value


class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ['id', 'budget_name', 'amount', 'description', 'created_at', 'updated_at']
    def validate_amount(self, value):
        if value <= 0:
            raise ValidationError("Amount must be greater than zero.")
        return value


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'user', 'amount', 'payment_method', 'recipient', 'status', 'transaction_id', 'gateway_response', 'created_at']
        read_only_fields = ['status', 'transaction_id', 'gateway_response', 'created_at']


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ['id', 'user', 'asset_type', 'symbol', 'quantity', 'purchase_price', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']