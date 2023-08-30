from django.db.models import TextChoices


class TransactionType(TextChoices):
    CREDIT = 'credit', 'credit'
    DEBIT = 'debit', 'debit'


class GenderType(TextChoices):
    MALE = 'male', 'male'
    FEMALE = 'female', 'female'
    OTHER = 'other', 'other'
    I_PREFER_NOT_TO_SAY = 'i_prefer_not_to_say', 'i_prefer_not_to_say'


class NotificationTypes(TextChoices):
    NOTIFICATION = 'notification', 'Notification'
    MESSAGE = 'message', 'Message'


class TransactionStatus(TextChoices):
    PENDING = 'pending', 'Pending'
    COMPLETED = 'completed', 'Completed'
    FAILED = 'failed', 'Failed'
    CANCELED = 'canceled', 'Canceled'
