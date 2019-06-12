import json
from django.shortcuts import get_object_or_404
from ..serializers import *
from ..models import Bar, User
from rest_framework import status, viewsets
from rest_framework.decorators import action
from .base import build_response
from ..util import Pagination
from ..util.truthy import is_true


SEARCHABLE_FIELDS = (
    'name', 'city',
)


def build_barmeta_query(request):
    queries = {}
    fields = []
    for field in BarMeta._meta.get_fields():
        if field.get_internal_type() == 'BooleanField':
            fields.append(field.name)
    for key, value in request.GET.items():
        if key in fields:
            queries["barmeta__%s" % (key)] = is_true(value)

    return queries




def build_barmeta_update(request, data, bar_meta):
    fields = []
    for field in BarMeta._meta.get_fields():
        if field.get_internal_type() == 'BooleanField':
            fields.append(field.name)

    for key, value in data.items():
        if key in fields:
            setattr(bar_meta, key, is_true(value))

        elif key in ('atmosphere', 'age_group', 'bar_type', 'happy_hour',
                       'popular_hours',):

                #take a list of ids from these and add them to barmeta
                model = None
                vals = []
                if key == 'atmosphere':
                    model = Atmosphere
                elif key == 'age_group':
                    model = AgeGroup
                elif key == 'bar_type':
                    model = BarType

                vals = model.objects.filter(id__in=value)
                t = getattr(bar_meta, key)
                t.set(vals)

        elif key in ('pricing', 'capacity', 'bar_stool_count',):
            setattr(bar_meta, key, value)

        bar_meta.save()

    return bar_meta

from .taggable import TaggableViewSet
class BarViewSet(TaggableViewSet):

    queryset = Bar.objects.all()
    pagination_class = Pagination
    paginate_by = 1
    paginate_by_param = 'page_size'
    max_paginate_by = 30

    def list(self, request):
        """return a list of bars, optionally matching a bunch of criteria"""

        args = {}
        queryset = Bar.objects.all()
        for key, val in request.GET.items():
            if key in SEARCHABLE_FIELDS:
                k = "%s__icontains" % (key)
                args[k] = val

        meta_args = build_barmeta_query(request)

        #only return bars with a rating higher than `min_rating`
        if 'min_rating' in request.GET:
            min_rating = request.GET.get('min_rating')
            bars = Bar.objects.all().annotate(avg_rating=Avg('barrating__rating'))\
                             .filter(avg_rating__gte=min_rating)\
                              .distinct()\
                              .values_list('id')

            args['id__in'] = bars

        args = {**args, **meta_args}

        if args:
            queryset = queryset.filter(**args)

        serializer = BarMiniSerializer(queryset, many=True)
        return build_response(request, serializer.data)

    def retrieve(self, request, pk=None):
        """return a single bar by id or hashid"""
        queryset = Bar.objects.all()
        bar = get_object_or_404(queryset, pk=pk)
        serializer = BarSerializer(bar)
        return build_response(request, serializer.data)

    def create(self, request):
        """create a new bar with minimal information"""
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        serializer = BarCreateSerializer(data=body)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        #now return the full bar
        s = BarSerializer(instance=serializer.instance)
        return build_response(request, s.data)

    #add/update meta info for a bar instance
    #this needs auth
    @action(detail=True, methods=['post'])
    def meta(self, request, pk=None):
        """add meta information to a bar"""
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        queryset = Bar.objects.all()
        bar = get_object_or_404(queryset, pk=pk)
        body['bar'] = bar.id
        if not hasattr(bar, 'barmeta'):
            #create a new bameta
            serializer = BarMetaCreateSerializer(data=body)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            bar.barmeta = serializer.instance
            bm = build_barmeta_update(request, body, serializer.instance)
            bm.save()
        else:
            #we are updating a barmeta
            bm = build_barmeta_update(request, body, bar.barmeta)
            bm.save()

        #now return the full bar
        s = BarSerializer(instance=bar)


    @action(detail=True,  methods=['get',])
    def checkins(self, request, pk=None):
        """list current checkins for a bar"""
        qs = Bar.objects.all()
        bar = get_object_or_404(qs, pk=pk)
        serializer = BarCheckinSerializer(bar.current_checkins, many=True)
        return build_response(request, serializer.data)


    @action(detail=True, methods=['post',])
    def checkin(self, request, pk=None):
        """checkin to a given bar"""
        #this needs lots of validation:
        #  such as not allowing overlapping checkins, etc...
        #  user validation, etc...
        user = request.user
        #we expect json of mood, doing, feeling
        #bar and user are determined from the request
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        queryset = Bar.objects.all()
        bar = get_object_or_404(queryset, pk=pk)
        checkin = BarCheckin(user=user, bar=bar)
        checkin.mood_id = body.get('mood', None)
        checkin.doing_id = body.get('doing', None)
        checkin.feeling_id = body.get('feeling', None)
        checkin.comment = body.get('comment', None)
        checkin.save()
        serializer = BarCheckinSerializer(instance=checkin)
        return build_response(request, serializer.data)
