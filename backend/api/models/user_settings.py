from django.contrib.gis.db import models
from django.db.models import Q, Sum, Avg
from django.utils import timezone
from hashid_field import HashidAutoField
from datetime import timedelta
from .base import BarRateTimestampModel
from .lookups import *
from .user import User


class UserSetting(BarRateTimestampModel):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    show_fullname = models.BooleanField(default=True)
    show_image = models.BooleanField(default=True)
    notifications = models.BooleanField(default=True)
    show_followers = models.BooleanField(default=True)

    class Meta:
        db_table = 'user_settings'
