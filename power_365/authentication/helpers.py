from dateutil.relativedelta import relativedelta
import datetime
from django.contrib.auth.hashers import check_password
from power_365.authentication.models import Pin


def verify_pin(user, pin):
    active_pin = Pin.objects.filter(user=user, active=True).first()
    if not active_pin:
        return False
    return check_password(pin, active_pin.code)


def get_date_range(start, end=40):
    end_year = datetime.datetime.now() - relativedelta(years=start)
    start_year = datetime.datetime.now() - relativedelta(years=end)
    return (start_year, end_year)
