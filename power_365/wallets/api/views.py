from rest_framework.response import Response
from rest_framework import generics
from power_365.wallets.api import serializers
from power_365.wallets import  models
from rest_framework.decorators import action, api_view, permission_classes, throttle_classes
from rest_framework.permissions import IsAuthenticated

class ListCurrencies(generics.ListAPIView):
    serializer_class = serializers.CurrencySerializer
    queryset = models.Currency.objects.all()
    pagination_class = None
    permission_classes = [IsAuthenticated]


currencies = ListCurrencies.as_view()


class CurrencyDetail(generics.RetrieveAPIView):
    serializer_class = serializers.CurrencySerializer
    queryset = models.Currency.objects.all()
    permission_classes = [IsAuthenticated]


currency = CurrencyDetail.as_view()


class ListTransactions(generics.ListAPIView):
    serializer_class = serializers.TransactionSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        return models.Transaction.objects.filter(user=self.request.user, is_active=True)


transactions = ListTransactions.as_view()


class TransactionDetail(generics.RetrieveAPIView):
    serializer_class = serializers.TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return models.Transaction.objects.filter(user=self.request.user)


transaction_detail = TransactionDetail.as_view()



class ListPayments(generics.ListAPIView):
    serializer_class = serializers.PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return models.Payment.objects.filter(user=self.request.user, is_active=True)


payments = ListPayments.as_view()


class PaymentDetail(generics.RetrieveAPIView):
    serializer_class = serializers.PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return models.Payment.objects.filter(user=self.request.user)


payment_detail = PaymentDetail.as_view()
