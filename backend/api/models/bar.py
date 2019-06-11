from django.contrib.gis.db import models
from django.db.models import Q, Sum, Avg
from django.utils import timezone
from hashid_field import HashidAutoField
from datetime import timedelta
from .base import BarRateModel, BarRateTaggableModel
from .lookups import *
from .user import User


class Bar(BarRateTaggableModel):
    id = HashidAutoField(allow_int_lookup=True, primary_key=True)
    name = models.CharField(max_length=255)
    location = models.PointField(null=True, blank=True)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100)
    state_province = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=25, null=True, blank=True)
    country = models.CharField(max_length=2, default='US')
    phone = models.CharField(max_length=30, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    neighborhood = models.ForeignKey(Neighborhood, on_delete=models.CASCADE,
                                     null=True, blank=True)

    @property
    def hours(self):
        return BarHours.objects.filter(bar=self)


    @property
    def meta(self):
        try:
            return BarMeta.objects.get(bar=self)
        except Exception as e:
            return None

    @property
    def happy_hour(self):
        return BarHappyHour.objects.filter(bar=self)

    @property
    def popular_hours(self):
        return BarPopularHours.objects.filter(bar=self)

    @property
    def recent_reviews(self):
        """return 5 most recent reviews"""
        return BarReview.objects.filter(bar=self).order_by('-created_at')[:5]

    @property
    def total_checkins(self):
        return BarCheckin.objects.filter(bar=self).count()

    @property
    def current_checkins(self):
        now = timezone.now()
        long_time = now - timedelta(hours=4)

        qs = BarCheckin.objects.filter(
            #Q(checkout__isnull=True) |
            (Q(created_at__gte=long_time) & Q(checkout__isnull=True))
        )
        return qs


    @property
    def checkins_today(self):
        pass

    @property
    def other_names(self):
        return BarAlsoKnownAs.objects.filter(bar=self)\
                             .order_by('name')\
                             .values_list()


    @property
    def rating(self):
        a = BarRating.objects.filter(bar=self)\
                             .aggregate(Avg('rating'))
        r = a['rating__avg']
        if r:
            return round(r*4)/4
        else:
            return None

    @property
    def images(self):
        return BarImage.objects.filter(bar=self)\
                               .order_by('-created_at')\
                               .values_list()
    class Meta:
        db_table = 'bar'


class BarHours(BarRateModel):
    bar = models.ForeignKey(Bar, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=3)
    open = models.TimeField()
    close = models.TimeField()

    class Meta:
        db_table = 'bar_hours'


class BarMeta(BarRateModel):
    bar = models.OneToOneField(Bar, on_delete=models.CASCADE)
    atmosphere = models.ManyToManyField(Atmosphere,
                                        blank=True)
    age_group = models.ManyToManyField(AgeGroup,
                                       blank=True)
    bar_info = models.ManyToManyField(BarInfo, blank=True)
    #eg, 4 would be '$$$$'
    pricing = models.IntegerField(blank=True, null=True)
    bar_type = models.ManyToManyField(BarType,
                                      blank=True)
    food = models.BooleanField(default=False)
    live_music = models.BooleanField(default=False)
    tvs = models.BooleanField(default=True)
    patio = models.BooleanField(default=False)
    tables = models.BooleanField(default=True)
    pool = models.BooleanField(default=False)
    shuffleboard = models.BooleanField(default=False)
    video_games = models.BooleanField(default=False)
    board_games = models.BooleanField(default=False)
    atm = models.BooleanField(default=False)
    pulltabs = models.BooleanField(default=False)
    chargers = models.BooleanField(default=False)
    jukebox = models.BooleanField(default=False)
    cash_only = models.BooleanField(default=False)
    kids = models.BooleanField(default=False)
    draft_beer = models.BooleanField(default=True)
    smoking_area = models.BooleanField(default=False)
    unisex_bathroom = models.BooleanField(default=False)
    schwag = models.BooleanField(default=False)
    capacity = models.IntegerField(null=True, blank=True)
    bar_stool_count = models.IntegerField(null=True, blank=True)
    popular_hours = models.ManyToManyField('BarPopularHours',
                                           blank=True)
    sports_bar = models.BooleanField(default=False)
    gay_friendly = models.BooleanField(default=True)
    sells_smokes = models.BooleanField(default=False)
    near_transit = models.BooleanField(default=True)
    historic = models.BooleanField(default=False)
    non_alchohol_friendly = models.BooleanField(default=True)
    local_beers = models.BooleanField(default=False)
    takes_amex = models.BooleanField(default=False)
    takes_discover = models.BooleanField(default=False)
    #is this a "locals" bar?
    local = models.BooleanField(default=False)
    wifi = models.BooleanField(default=True)
    first_call = models.BooleanField(default=False)
    happy_hour = models.ManyToManyField('BarHappyHour', blank=True)

    class Meta:
        db_table = 'bar_meta'


class BarHappyHour(BarRateTaggableModel):
    bar = models.ForeignKey(Bar, on_delete=models.CASCADE)
    start = models.TimeField()
    end = models.TimeField()
    note = models.CharField(max_length=512)

    class Meta:
        db_table = 'bar_happy_hour'


class BarPopularHours(BarRateTaggableModel):
    bar = models.ForeignKey(Bar, on_delete=models.CASCADE)
    start = models.TimeField()
    end = models.TimeField()

    class Meta:
        db_table = 'bar_popular_hours'


class BarReview(BarRateTaggableModel):
    bar = models.ForeignKey(Bar, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.CharField(max_length=2048)
    rating = models.IntegerField(null=True, blank=True)
    public = models.BooleanField(default=True)

    class Meta:
        db_table = 'bar_review'


class BarCheckin(BarRateModel):
    bar = models.ForeignKey(Bar, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=512, null=True, blank=True)
    mood = models.ForeignKey(Mood, null=True, blank=True, on_delete=models.CASCADE)
    public = models.BooleanField(default=True)
    doing = models.ForeignKey(Doing, null=True, blank=True, on_delete=models.CASCADE)
    feeling = models.ForeignKey(Feeling, null=True, blank=True, on_delete=models.CASCADE)
    checkout = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'bar_checkin'

class BarWith(BarRateModel):
    bar_checkin = models.ForeignKey(BarCheckin, on_delete=models.CASCADE)
    with_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, null=True, blank=True)
    public = models.BooleanField(default=True)

    class Meta:
        db_table = 'bar_with'


class BarDrinking(BarRateModel):
    """what the user is drinking during this checkin"""
    bar_checkin = models.ForeignKey(BarCheckin, on_delete=models.CASCADE)
    drink = models.ForeignKey(Drink, on_delete=models.CASCADE)
    public = models.BooleanField(default=True)

    class Meta:
        db_table = 'bar_drinking'


class BarAlsoKnownAs(BarRateModel):
    bar = models.ForeignKey(Bar, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    closed_year = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'bar_also_known_as'


class BarRating(BarRateModel):
    bar = models.ForeignKey(Bar, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=3, decimal_places=2)

    class Meta:
        db_table = 'bar_rating'

def image_upload_path(instance, filename):
    return "bar/official/{0}/{1}".format(instance.bar.id, filename)


class BarImage(BarRateTaggableModel):
    bar = models.ForeignKey(Bar, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=image_upload_path, max_length=255)
