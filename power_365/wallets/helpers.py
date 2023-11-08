from decimal import Decimal
from power_365.wallets import choices
from power_365.wallets.models import Transaction
from django.db import models

def user_balance(self, user):
        total_deposit = Transaction.objects.filter(
            currency=self,  user=user, tx_type=choices.TransactionTypes.CREDIT, status=choices.StatusChoices.CONFIRMED, is_active=True).aggregate(models.Sum('amount'))
        total_withdrawal = Transaction.objects.filter(
            models.Q( status=choices.StatusChoices.CONFIRMED) | models.Q( status=choices.StatusChoices.PENDING),
            currency=self, user=user, tx_type=choices.TransactionTypes.DEBIT, is_active=True).aggregate(models.Sum('amount'))
        deposit_amount = total_deposit.get('amount__sum') or Decimal(0.0)
        withdraw_amount = total_withdrawal.get('amount__sum') or Decimal(0.0)
        return deposit_amount - withdraw_amount
