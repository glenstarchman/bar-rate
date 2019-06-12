from rest_framework import serializers
from hashid_field.rest import HashidSerializerCharField
from ..models import *
from .user import MiniUserSerializer
from .bar import BarSerializer, BarMiniSerializer
from .taggable_serializer import *

class BartenderSerializer(TaggableSerializer):

    bars = BarMiniSerializer('bar', many=True)
    user = MiniUserSerializer()
    class Meta:
        model = Bartender
        fields = TaggableSerializer.Meta.fields + ['name', 'nickname', 'gender',
                  'user', 'bars', 'schedule',
                  'hot',]
