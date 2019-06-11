from .lookups import *

def _add_lookup(model, values):
    for value in values:
        if (model.objects.filter(name=value).count() == 0):
            obj = model(name=value)
            obj.save()

def add_gender():
    _add_lookup(Gender, GENDERS)

def add_atmosphere():
    _add_lookup(Atmosphere, ATMOSPHERES)

def add_doing():
    _add_lookup(Doing, DOING)

def add_drink():
    _add_lookup(Drink, DRINKS)

def add_mood():
    _add_lookup(Mood, MOODS)

def add_age_group():
    _add_lookup(AgeGroup, AGE_GROUPS)

def add_music_genre():
    _add_lookup(MusicGenre, MUSIC_GENRES)

def add_feeling():
    _add_lookup(Feeling, FEELING)


def add_bar_type():
    _add_lookup(BarType, BAR_TYPES)


def insert_lookups(apps=None, schema_editor=None):
    add_bar_type()
    add_feeling()
    add_music_genre()
    add_age_group()
    add_mood()
    add_drink()
    add_atmosphere()
    add_doing()
    add_gender()
