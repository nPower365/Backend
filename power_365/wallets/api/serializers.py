from rest_framework import serializers
from power_365.wallets import models


class CurrencySerializer(serializers.ModelSerializer):
    balance = serializers.SerializerMethodField(
        method_name='get_user_balance')

    def get_user_balance(self, instance):
        user = self.context.get('request').user
        balance = instance.user_balance(user)
        return {
            'currency': instance.symbol,
            'currency_amount': balance,
        }

    class Meta:
        model = models.Currency
        fields = (
            'id',
            'name',
            'symbol',
            'balance',
        )


class CurrencyDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Currency
        fields = (
            'id',
            'name',
            'symbol',
        )


class TransactionSerializer(serializers.ModelSerializer):
    currency = CurrencyDetailSerializer(read_only=True)

    class Meta:
        model = models.Transaction
        fields = "__all__"

class PaymentSerializer(serializers.ModelSerializer):
    currency = CurrencyDetailSerializer(read_only=True)
    transaction = TransactionSerializer(read_only=True)

    class Meta:
        model = models.Payment
        fields = "__all__"
