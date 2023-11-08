from decimal import Decimal
from django.db import models
from power_365.core.models import Country

from power_365.utils.model_utils import BaseModel
from power_365.wallets import choices
from django.contrib.auth import get_user_model
User = get_user_model()



class Currency(BaseModel):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=10, blank=True, null=True)
    symbol = models.CharField(max_length=200)
    country = models.OneToOneField('core.Country', on_delete=models.CASCADE, related_name="country")
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.code

    # get the user balance in selected currency
    def user_balance(self, user):
        total_deposit = Transaction.objects.filter(
            currency=self,  user=user, tx_type=choices.TransactionTypes.CREDIT, status=choices.StatusChoices.CONFIRMED, is_active=True).aggregate(models.Sum('amount'))
        total_withdrawal = Transaction.objects.filter(
            models.Q( status=choices.StatusChoices.CONFIRMED) | models.Q( status=choices.StatusChoices.PENDING),
            currency=self, user=user, tx_type=choices.TransactionTypes.DEBIT, is_active=True).aggregate(models.Sum('amount'))
        deposit_amount = total_deposit.get('amount__sum') or Decimal(0.0)
        withdraw_amount = total_withdrawal.get('amount__sum') or Decimal(0.0)
        return deposit_amount - withdraw_amount

    class Meta:
        ordering = ["name"]



class Gateway(BaseModel):

    name = models.CharField(unique=True, max_length=255)
    type = models.CharField(
        max_length=255, choices=choices.GatewayTypeChoices.choices, default=choices.GatewayTypeChoices.PAYMENT)
    configurations = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Bank(BaseModel):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10)
    gateway = models.ForeignKey(
        Gateway, on_delete=models.CASCADE, related_name="banks")
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name="banks")
    def __str__(self):
        return self.name


class PaymentMethod(BaseModel):
    name = models.CharField(max_length=200)
    active = models.BooleanField(default=1)
    country = models.ForeignKey(
        Country, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Transaction(BaseModel):
    user = models.ForeignKey(User,
                             on_delete=models.RESTRICT)

    currency = models.ForeignKey(Currency,
                             on_delete=models.RESTRICT)
    tx_type = models.CharField(choices=choices.TransactionTypes.choices,
                            max_length=32, default=choices.TransactionTypes)
    channel = models.CharField(
        max_length=32, choices=choices.TransactionChannels.choices, default=choices.TransactionChannels.PAYMENT)
    amount = models.DecimalField(max_digits=14, decimal_places=4)
    description = models.TextField(null=True, blank=True)
    fee = models.DecimalField(max_digits=14, decimal_places=4)
    delivery_request = models.ForeignKey(
        'delivery.DeliveryRequest', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(
        max_length=255, choices=choices.StatusChoices.choices, default=choices.StatusChoices.PENDING)

    def __str__(self):
        return "{} to {}: ({} {})".format(self.description, self.user.fullname, self.amount, self.type)

    class Meta:
        ordering = ["-date_created"]

class Payment(BaseModel):
    amount = models.DecimalField(max_digits=14, decimal_places=4)
    reference = models.CharField(max_length=255, unique=True)
    email = models.EmailField()
    payment_method = models.ForeignKey(
        PaymentMethod, on_delete=models.SET_NULL, null=True)
    gateway = models.ForeignKey(
        Gateway, on_delete=models.SET_NULL, null=True)
    gateway_reference = models.CharField(max_length=255, null=True, blank=True)
    gateway_fee = models.DecimalField(
        max_digits=14, decimal_places=4)
    status = models.CharField(
        max_length=255, choices=choices.PaymentStatusChoices.choices, default=choices.PaymentStatusChoices.PENDING)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction = models.ForeignKey(
        Transaction, on_delete=models.SET_NULL, blank=True, null=True)
    delivery_request = models.ForeignKey('delivery.DeliveryRequest', blank=True, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField('created at', auto_now_add=True)
    updated_at = models.DateTimeField(' updated at', auto_now=True)

    def __str__(self):
        return "Payment for {} - {}".format(self.delivery_request.name, self.reference) if self.delivery_request else 'Deposit'

    class Meta:
        ordering = ["-date_created"]

# class Withdrawal(BaseModel):
#     amount = models.DecimalField(max_digits=14, decimal_places=4,
#                         default_currency='USD')
#     user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#     transaction = models.ForeignKey(
#         Transaction, on_delete=models.SET_NULL, null=True)
#     reference = models.CharField(max_length=255, unique=True)
#     gateway = models.ForeignKey(
#         Gateway, on_delete=models.SET_NULL, null=True)
#     gateway_reference = models.CharField(max_length=255, null=True, blank=True)
#     gateway_fee = models.DecimalField(max_digits=14, decimal_places=4)
#     status = models.CharField(
#         max_length=255, choices=choices.StatusChoices.choices, default=choices.StatusChoices.PENDING)
#     account_name = models.CharField(max_length=255)
#     account_number = models.CharField(max_length=32)
#     bank_id = models.CharField(max_length=32)

