from rest_framework import serializers
from hashid_field.rest import HashidSerializerCharField
from ..models.user import User
from ..models.profile import Profile
from .bartender import MiniBartenderSerializer
from .mini_serializers import MiniBarSerializer, MiniUserSerializer
from .lookups import *
from .taggable_serializer import *

class ProfileSerializer(serializers.ModelSerializer):
    gender = GenderSerializer()
    class Meta:
        model = Profile
        fields = ('gender', 'timezone', 'image', 'headline', 'blurb',
                  'city', 'state_province',)



class FullProfileSerializer(serializers.ModelSerializer):
    id = HashidSerializerCharField()
    #user = MiniUserSerializer()
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
        fields = [
            'id', 'gender', 'timezone', 'image', 'headline', 'blurb',
            'city', 'state_province',
            'favorite_bars', 'favorite_bartenders',
            'favorite_music_genres', 'interested_in_genders',
            'interested_in_age_groups', 'favorite_bar_types',
            'image', 'birthdate', 'relationship_status'
        ]


class UserSerializer(TaggableSerializer):
    id = HashidSerializerCharField()
    current_checkin = serializers.SerializerMethodField()
    profile = FullProfileSerializer()
    recent_user_likes = LikeSerializer(many=True)
    recent_user_reviews = ReviewSerializer(many=True)
    recent_user_comments = CommentSerializer(many=True)

    def get_current_checkin(self, instance):
        from .bar import MiniBarCheckinSerializer
        return MiniBarCheckinSerializer(instance.current_checkin).data

    class Meta:
        model = User
        fields = TaggableSerializer.Meta.fields + [
            'id', 'username', 'first_name', 'last_name',
            'profile', 'user_likes_count', 'user_dislikes_count',
            'user_comments_count', 'current_checkin',
            'recent_user_likes', 'recent_user_reviews',
            'recent_user_comments', 'user_following_count', 'follower_count',
        ]
