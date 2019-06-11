from django.contrib.gis.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from hashid_field import HashidAutoField
from .base import BarRateModel, BarRateTaggableModel
from .lookups import *
from .bar import Bar
from .user import User


class Bartender(BarRateTaggableModel):
    id = HashidAutoField(allow_int_lookup=True, primary_key=True)
    name = models.CharField(max_length=120)
    nickname = models.CharField(max_length=32, null=True)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             null=True, blank=True)
    bars = models.ManyToManyField(Bar, blank=True)

    @property
    def schedule(self):
        ret = {}
        schedules = BartenderSchedule.objects.filter(bartender=self)
        if schedules.count() == 0:
            return None

        for schedule in schedules:
            key = str(bar.id)
            data = {
                'day': schedule.day_of_week,
                'open': schedule.open,
                'close': schedule.close
            }
            if not key in ret:
                ret[key] = [data]
            else:
                ret[key].append(data)
        return ret

    @property
    def recent_reviews(self):
        return BartenderReview.objects.filter(
            bartender=self,
            public=True
        ).order_by('-created_at')[:5]

    @property
    def hot(self):
        qs = BartenderHotVote.objects.filter(bartender=self)
        total = qs.count()
        hot_count = qs.filter(hot=True).count()
        if total > 0 and hot_count > 0:
            p = round((hot_count/total) * 4, 2)/4
            percent =  "{:.2%}".format(p)

            if percent.endswith('.00%'):
                #strip it off
                percent = "%s%%" % (percent[:-4])
            return {
                "percent": percent,
                "total_votes": total,
                "hot_votes": hot_count
            }
        return None

    class Meta:
        db_table = 'bartender'


class BartenderSchedule(BarRateModel):
    """a schedule per-day, per-bartender, per-bar"""
    bartender = models.ForeignKey(Bartender, null=True, blank=True, on_delete=models.CASCADE)
    bar = models.ForeignKey(Bar, null=True, blank=True, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=3)
    open = models.TimeField()
    close = models.TimeField()

    class Meta:
        db_table = 'bartender_schedule'

class BartenderReview(BarRateModel):
    bartender = models.ForeignKey(Bartender, on_delete=models.CASCADE)
    bar = models.ForeignKey(Bar, null=True, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.CharField(max_length=2048, null=True, blank=True)
    rating = models.IntegerField(blank=True, null=True)
    public = models.BooleanField(default=True)

    class Meta:
        db_table = 'bartender_review'


class BartenderHotVote(BarRateModel):
    bartender = models.ForeignKey(Bartender, on_delete=models.CASCADE)
    hot = models.BooleanField()

    class Meta:
        db_table = 'bartender_hot_vote'


def your_receiver_function(sender, instance, *args, **kwargs):
      if instance.title and not instance.slug:
               instance.slug = slugify(instance.title)

def generate_nickname(sender, instance, *args, **kwargs):
    if not instance.nickname:
        #firstname+firstletter_of_last_name
        s = instance.name.split(' ')
        if len(s) > 1:
            s = "%s%s" % (s[0].capitalize(), s[-1].capitalize()[:1])[:31]
        else:
            s = s.capitalize()[:31]

        instance.nickname = s


pre_save.connect(generate_nickname, sender=Bartender)
