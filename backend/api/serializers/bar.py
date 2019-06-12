from rest_framework import serializers
from hashid_field.rest import HashidSerializerCharField
from ..models import *
from .user import MiniUserSerializer


class MoodSerializer(serializers.ModelSerializer):

    id = HashidSerializerCharField()
    class Meta:
        model = Mood
        fields = ('id', 'name',)

class DoingSerializer(serializers.ModelSerializer):

    id = HashidSerializerCharField()
    class Meta:
        model = Doing
        fields = ('id', 'name',)

class FeelingSerializer(serializers.ModelSerializer):

    id = HashidSerializerCharField()

    class Meta:
        model = Feeling
        fields = ('id', 'name',)

class AtmosphereSerializer(serializers.ModelSerializer):

    id = HashidSerializerCharField()
    class Meta:
        model = Atmosphere
        fields = ('id', 'name',)

class AgeGroupSerializer(serializers.ModelSerializer):

    id = HashidSerializerCharField()
    class Meta:
        model = AgeGroup
        fields = ('id', 'name')

class BarInfoSerializer(serializers.ModelSerializer):

    id = HashidSerializerCharField()
    class Meta:
        model = BarInfo
        fields = ('id', 'name', 'value',)

class HappyHourSerializer(serializers.ModelSerializer):

    class Meta:
        model = BarHappyHour
        fields = ('start', 'end',)

class PopularHourSerializer(serializers.ModelSerializer):

    class Meta:
        model = BarPopularHours
        fields = ('start', 'end',)

class BarHourSerializer(serializers.ModelSerializer):

    id = HashidSerializerCharField()
    class Meta:
        model = BarHours
        fields = ('id', 'day_of_week', 'open', 'close',)

class BarTypeSerializer(serializers.ModelSerializer):

    id = HashidSerializerCharField()
    class Meta:
        model = BarType
        fields = ('id', 'name',)


class BarMetaSerializer(serializers.ModelSerializer):

    atmosphere = AtmosphereSerializer(many=True, required=False)
    age_group = AgeGroupSerializer(many=True, required=False)
    bar_info = BarInfoSerializer(many=True, required=False)
    bar_type = BarTypeSerializer(many=True, required=False)
    popular_hours = PopularHourSerializer(many=True, required=False)
    happy_hour = HappyHourSerializer(many=True, required=False)

    class Meta:
        model = BarMeta
        #fields = "__all__"
        exclude = ('id', 'bar',)

class BarMetaCreateSerializer(serializers.ModelSerializer):

    atmosphere = AtmosphereSerializer(many=True, required=False)
    age_group = AgeGroupSerializer(many=True,required=False)
    bar_info = BarInfoSerializer(required=False)
    #bar_type = BarTypeSerializer(required=False)
    popular_hours = PopularHourSerializer(required=False)
    happy_hour = HappyHourSerializer(required=False)

    class Meta:
        model = BarMeta
        #fields = "__all__"
        exclude = ('id', )


class BarCheckinSerializer(serializers.ModelSerializer):

    user = MiniUserSerializer()
    mood = MoodSerializer()
    doing = DoingSerializer()
    feeling = FeelingSerializer()
    created_at = serializers.DateTimeField(required=False)

    class Meta:
        model = BarCheckin
        fields = ('user', 'comment', 'mood', 'doing',
                  'feeling', 'created_at', )


class BarReviewSerializer(serializers.ModelSerializer):

    user = MiniUserSerializer()
    created_at = serializers.DateTimeField()

    class Meta:
        model = BarReview
        fields = ('user', 'review', 'rating', 'created_at')

class BarSerializer(serializers.ModelSerializer):

    id = HashidSerializerCharField()
    location = serializers.ReadOnlyField()
    hours = BarHourSerializer(many=True)
    meta = BarMetaSerializer()
    current_checkins = BarCheckinSerializer(many=True)

    class Meta:
        model = Bar
        fields = ('id', 'name', 'location', 'address1', 'address2', 'city',
                  'state_province', 'postal_code', 'country',
                  'phone', 'email', 'hours', 'meta', 'happy_hour',
                  'popular_hours', 'recent_reviews', 'total_checkins',
                  'current_checkins', 'images', 'other_names', 'rating',
        )


class BarCreateSerializer(serializers.ModelSerializer):


    class Meta:
        model = Bar
        fields = ('name', 'address1', 'address2', 'city',
                'state_province', 'country', 'phone',
                'email',)

class BarMiniSerializer(serializers.ModelSerializer):

    id = HashidSerializerCharField()
    location = serializers.ReadOnlyField()
    current_checkins = BarCheckinSerializer(many=True)
    #hours = BarHourSerializer(many=True)

    class Meta:
        model = Bar

        fields = ('id', 'name', 'location',
                  'address1', 'address2', 'city',
                  'state_province', 'postal_code', 'country',
                  'phone', 'email',
                  'total_checkins',
                  'images', 'rating', 'current_checkins',
        )

class MiniBarCheckinSerializer(serializers.ModelSerializer):

    bar = BarMiniSerializer()
    mood = MoodSerializer()
    doing = DoingSerializer()
    feeling = FeelingSerializer()
    created_at = serializers.DateTimeField(required=False)

    class Meta:
        model = BarCheckin
        fields = ('bar', 'comment', 'mood', 'doing',
                  'feeling', 'created_at', )
