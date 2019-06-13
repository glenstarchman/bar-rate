
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
from .lookups import *
from .bar import Bar
from .bartender import Bartender


class Profile(BarRateTaggableModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name = "profile")
    gender = models.ForeignKey(Gender, null=True, blank=True, on_delete=models.CASCADE)
    timezone = models.IntegerField(null = True, blank = True, default=-8)
    image = models.URLField(max_length = 512, blank = True, null = True)
    headline = models.CharField(max_length=140)
    blurb = models.CharField(max_length=1024, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state_province = models.CharField(max_length=120, blank=True, null=True)
    country = models.CharField(max_length=3, null=True, blank=True, default="USA")
    favorite_bars = models.ManyToManyField(Bar, related_name='favorite_bars')
    favorite_bartenders = models.ManyToManyField(Bartender, related_name='favorite_bartenders')
    favorite_music_genres = models.ManyToManyField(MusicGenre, related_name='favorite_music_genres')
    interested_in_genders = models.ManyToManyField(Gender, related_name='interested_in_genders')
    interested_in_age_groups = models.ManyToManyField(AgeGroup, related_name='interested_in_age_groups')
    favorite_bar_types = models.ManyToManyField(BarType, related_name='favorite_bar_types')
    image = models.URLField(null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    relationship_status = models.ForeignKey(RelationshipStatus, null=True, blank=True, on_delete=models.CASCADE)



    def __repr__(self):
        return "<Profile: %s>" % (self.user.username[:20])

    class Meta:
        db_table = "profile"
