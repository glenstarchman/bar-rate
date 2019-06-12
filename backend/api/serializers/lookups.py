from rest_framework import serializers
from hashid_field.rest import HashidSerializerCharField
from ..models import *
from .taggable_serializer import TaggableSerializer


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

class GenderSerializer(serializers.ModelSerializer):

    id = HashidSerializerCharField()
    class Meta:
        model = Gender
        fields = ('id', 'name')

class MusicGenreSerializer(serializers.ModelSerializer):

    id = HashidSerializerCharField()
    class Meta:
        model = MusicGenre
        fields = ('id', 'name')

class BarTypeSerializer(serializers.ModelSerializer):

    id = HashidSerializerCharField()
    class Meta:
        model = BarType
        fields = ('id', 'name',)

class RelationshipStatusSerializer(serializers.ModelSerializer):

    id = HashidSerializerCharField()
    class Meta:
        model = RelationshipStatus
        fields = ('id', 'name',)
