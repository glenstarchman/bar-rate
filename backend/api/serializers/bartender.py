from rest_framework import serializers
from hashid_field.rest import HashidSerializerCharField
from ..models import *
from .taggable_serializer import *
from .mini_serializers import MiniBarSerializer, MiniUserSerializer

class BartenderSerializer(TaggableSerializer):

    bars = MiniBarSerializer('bar', many=True)
    user = MiniUserSerializer()
    class Meta:
        model = Bartender
        fields = TaggableSerializer.Meta.fields + ['name', 'nickname', 'gender',
                  'user', 'bars', 'schedule',
                  'hot',]


class MiniBartenderSerializer(serializers.ModelSerializer):

    bars = MiniBarSerializer('bar', many=True)
    class Meta:
        model = Bartender
        fields = ['name', 'nickname', 'gender',
                  'bars',]
