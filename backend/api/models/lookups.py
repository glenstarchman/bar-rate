from django.contrib.gis.db import models
from .base import BarRateModel

GENDERS = [
    'Man',
    'Woman',
    'MtF',
    'FtM',
    'Genderqueer',
    'Not Specified',
]

ATMOSPHERES = [



]

DOING = [
    'Drinking Beer',
    'Drinking Alcohol',

]

FEELING = [
    'Happy',
    'Sad',
    'Emotional',
    'Depressed',
    'Angry',
    'Blessed',
    'Pissed Off',
    ''

]


DRINKS = [


]


MOODS = [


]

AGE_GROUPS = [
    'Under 21',
    '21 - 25',
    '26 - 30',
    '31 - 35',
    '36 - 45',
    '45 - 55',
    '55+',
]


MUSIC_GENRES = [


]

BAR_TYPES = [
    'Dive',
    'Pub',
    'Gastropub',
    'Brewpub',
    'Brewery',
    'Cigar',
    'Irish',
    'English',
    'Australian',
    'Asian',
    'European',
    'Sports',
    'College',
    'Craft ',
    'Hotel',
    'Fancy',
    'Meat Market',
    'Singles',
    'Gaming',
    'Whiskey',
    'Distillery',
]


class Gender(BarRateModel):
    name = models.CharField(max_length=30)
    value = models.CharField(max_length=1, null=True, blank=True)

    class Meta:
        db_table = 'gender'


class Atmosphere(BarRateModel):
    name = models.CharField(max_length=30)

    class Meta:
        db_table = 'atmosphere'



class Doing(BarRateModel):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'doing'


class Drink(BarRateModel):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'drink'

class Mood(BarRateModel):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'mood'

class AgeGroup(BarRateModel):
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'age_group'


class MusicGenre(BarRateModel):
    name = models.CharField(max_length=120)

    class Meta:
        db_table = 'music_genre'


class Feeling(BarRateModel):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'feeling'


class BarType(BarRateModel):
    """eg: craft, dive, pub, etc..."""
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'bar_type'


class BarInfo(BarRateModel):
    """unstructured key/values about bar"""
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

    class Meta:
        db_table = 'bar_info'


class Neighborhood(BarRateModel):
    city = models.CharField(max_length=200)
    state_or_province = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
