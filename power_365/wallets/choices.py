from django.db.models import TextChoices


class TransactionTypes(TextChoices):
    CREDIT = 'credit', 'credit'
    DEBIT = 'debit', 'debit'


class TransactionChannels(TextChoices):
    DEPOSIT = 'deposit', 'deposit'
    WITHDRAWAL = 'withdrawal', 'withdrawal'
    PAYMENT = 'payment', 'payment'
    REFERRAL_BONUS = 'referral_bonus', 'referral_bonus'


class StatusChoices(TextChoices):
    PENDING = 'pending', 'pending'
    CONFIRMED = 'confirmed', 'confirmed'
    FAILED = 'failed', 'failed'


class PaymentStatusChoices(TextChoices):
    PENDING = 'pending', 'pending'
    APPROVED = 'approved', 'approved'
    FAILED = 'failed', 'failed'

class GatewayTypeChoices(TextChoices):
    PAYMENT = 'payment', 'payment'
