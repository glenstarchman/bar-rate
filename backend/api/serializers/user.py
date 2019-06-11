from rest_framework import serializers
from hashid_field.rest import HashidSerializerCharField
from ..models.user import User


class MiniUserSerializer(serializers.ModelSerializer):

    id = HashidSerializerCharField()
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name',)
