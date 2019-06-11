#helpers for handling check ins
from django.utils import timezone
from django.db.models import Q
from datetime import timedelta
from ..models import User, Bar, BarCheckin


def is_checked_in_here(user, bar):
    #is this user already checked in to this bar?
    bc = BarCheckin.objects.filter(
        user = user,
        bar = bar,
        checkout__isnull=True
    )

    if bc.count() > 0:
        return True
    else:
        return False


def auto_checkout(user):
    #if the user is checked in somewhere else
    #then check them out of that place
    now = timezone.now()
    long_time = now - timedelta(hours=4)
    qs = BarCheckin.objects.filter(
        Q(user=user) &
        (Q(created_at__lte=long_time) & Q(checkout__isnull=True))
    )
    for q in qs:
        q.checkout = timezone.now()
        q.save()
