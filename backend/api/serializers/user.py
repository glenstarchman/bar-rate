from rest_framework import serializers
from hashid_field.rest import HashidSerializerCharField
from ..models.user import User
from ..models.profile import Profile

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('gender', 'timezone', 'image', 'headline', 'blurb',
                  'city', 'state_province',)


class UserSerializer(serializers.ModelSerializer):
    id = HashidSerializerCharField()
    profile = ProfileSerializer()
    current_checkin = serializers.SerializerMethodField()

    def get_current_checkin(self, instance):
        from .bar import MiniBarCheckinSerializer
        print("here")
        return MiniBarCheckinSerializer(instance.current_checkin).data

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name',
                  'profile', 'user_likes_count', 'user_dislikes_count',
                  'user_comments_count', 'current_checkin', )

class MiniUserSerializer(serializers.ModelSerializer):

    id = HashidSerializerCharField()
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name',
                  'profile', )
