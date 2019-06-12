from rest_framework import serializers
from hashid_field.rest import HashidSerializerCharField
from ..models import *
from .taggable_serializer import TaggableSerializer
from .lookups import *

class MiniBarSerializer(serializers.ModelSerializer):

    id = HashidSerializerCharField()
    location = serializers.ReadOnlyField()
    #current_checkins = BarCheckinSerializer(many=True)
    #hours = BarHourSerializer(many=True)

    class Meta:
        model = Bar

        fields = ('id', 'name', 'location',
                  'address1', 'address2', 'city',
                  'state_province', 'postal_code', 'country',
                  'phone', 'email',
                  'total_checkins',
                  'rating', 'current_checkins',
        )

class MiniBarCheckinSerializer(serializers.ModelSerializer):

    bar = MiniBarSerializer()
    mood = MoodSerializer()
    doing = DoingSerializer()
    feeling = FeelingSerializer()
    created_at = serializers.DateTimeField(required=False)

    class Meta:
        model = BarCheckin
        fields = ('bar', 'comment', 'mood', 'doing',
                  'feeling', 'created_at', )

class MiniUserSerializer(serializers.ModelSerializer):

    id = HashidSerializerCharField()
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name',
                  )
