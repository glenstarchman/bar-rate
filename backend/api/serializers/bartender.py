from rest_framework import serializers
from hashid_field.rest import HashidSerializerCharField
from ..models import *
from .user import MiniUserSerializer
from .bar import BarSerializer, BarMiniSerializer



class BartenderReviewSerializer(serializers.ModelSerializer):

    user = MiniUserSerializer()

    class Meta:
        model = BartenderReview
        fields = ('user', 'review', 'rating', 'created_at',)



class BartenderSerializer(serializers.ModelSerializer):

    id = HashidSerializerCharField()
    bars = BarMiniSerializer('bar', many=True)
    user = MiniUserSerializer()
    recent_reviews = BartenderReviewSerializer(many=True, read_only=True,
                                               required=False)

    class Meta:
        model = Bartender
        fields = ('id', 'name', 'nickname', 'gender',
                  'user', 'bars', 'schedule',
                  'recent_reviews', 'hot',)
