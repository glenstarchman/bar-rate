from dateutil.relativedelta import relativedelta
from django.utils import timezone


def get_month_day_range(date=None):
    """
    For a date 'date' returns the start and end date for the month of 'date'.
    Month with 31 days:
    >>> date = datetime.date(2011, 7, 27)
    >>> get_month_day_range(date)
    (datetime.date(2011, 7, 1), datetime.date(2011, 7, 31))
    Month with 28 days:
    >>> date = datetime.date(2011, 2, 15)
    >>> get_month_day_range(date)
    (datetime.date(2011, 2, 1), datetime.date(2011, 2, 28))
    """
    if not date:
        date = timezone.now()

    last_day = date + relativedelta(day=1, months=+1, days=-1)
    first_day = date + relativedelta(day=1)
    return first_day, last_day


def get_range(start_date=None, end_date=None):
    if not start_date and not end_date:
        return get_month_day_range()
    if not end_date and start_date:
        end_date = start_date + relativedelta(day=1, months=+1, days=-1)

    if not start_date:
        start_date = timezone.no() - relativedelta(day=1, months=-1, days=-1)

    return start_date, end_date
