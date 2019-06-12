from rest_framework import serializers
from hashid_field.rest import HashidSerializerCharField
from ..models.user import User
from ..models.profile import Profile
from .bartender import MiniBartenderSerializer
from .mini_serializers import MiniBarSerializer, MiniUserSerializer
from .lookups import *
from .taggable_serializer import TaggableSerializer

class ProfileSerializer(serializers.ModelSerializer):
    gender = GenderSerializer()
    class Meta:
        model = Profile
        fields = ('gender', 'timezone', 'image', 'headline', 'blurb',
                  'city', 'state_province',)



class FullProfileSerializer(TaggableSerializer):
    id = HashidSerializerCharField()
    user = MiniUserSerializer()
    gender = GenderSerializer()
    favorite_bars = MiniBarSerializer(many=True)
    favorite_bartenders = MiniBartenderSerializer(many=True)
    favorite_music_genres = MusicGenreSerializer(many=True)
    interested_in_genders = GenderSerializer(many=True)
    interested_in_age_groups = AgeGroupSerializer(many=True)
    favorite_bar_types = BarTypeSerializer(many=True)
    relationship_status = RelationshipStatusSerializer()

    class Meta:
        model = Profile
        fields = TaggableSerializer.Meta.fields + [
            'user', 'gender', 'timezone', 'image', 'headline', 'blurb',
            'city', 'state_province',
            'favorite_bars', 'favorite_bartenders',
            'favorite_music_genres', 'interested_in_genders',
            'interested_in_age_groups', 'favorite_bar_types',
            'image', 'birthdate', 'relationship_status'
        ]


class UserSerializer(serializers.ModelSerializer):
    id = HashidSerializerCharField()
    current_checkin = serializers.SerializerMethodField()

    def get_current_checkin(self, instance):
        from .bar import MiniBarCheckinSerializer
        return MiniBarCheckinSerializer(instance.current_checkin).data

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name',
                  'profile', 'user_likes_count', 'user_dislikes_count',
                  'user_comments_count', 'current_checkin', )
