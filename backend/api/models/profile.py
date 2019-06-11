
from django.db import models
from django.db.models.signals import pre_save
from django.db.models import Q
from django.conf import settings
import datetime
import time
from inflection import titleize
import json

from .base import *
from .user import User
from .lookups import Gender


class Profile(BarRateModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name = "profile")
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    timezone = models.IntegerField(null = True, blank = True, default=-8)
    image = models.URLField(max_length = 512, blank = True, null = True)
    headline = models.CharField(max_length=140)
    blurb = models.CharField(max_length=1024)
    city = models.CharField(max_length=255)
    state_province = models.CharField(max_length=120)

    def __repr__(self):
        return "<Profile: %s>" % (self.user.name[:20])

    class Meta:
        db_table = "profile"
