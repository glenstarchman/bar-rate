from rest_framework import serializers
from hashid_field.rest import HashidSerializerCharField
from ..models.user import User
from ..models.taggable import *
from ..models.bar import Bar
from ..models.bartender import Bartender


class ReprMixin(object):

    def get_obj(self, obj):
        from .mini_serializers import (MiniBarSerializer, MiniUserSerializer)
        from .bartender import MiniBartenderSerializer
        o = obj.content_object
        serializer = None
        obj_type = None
        if isinstance(o, Bar):
            serializer = MiniBarSerializer
            obj_type = 'bar'
        elif isinstance(o, Bartender):
            serializer = MiniBartenderSerializer
            obj_type = 'bartender'
        elif isinstance(o, User):
            serializer = MiniUserSerializer
            obj_type = 'user'


        d = serializer(instance=o).data
        d['type'] = obj_type
        return d


class TaggableUserSerializer(serializers.ModelSerializer):
    id = HashidSerializerCharField()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username',)


class CommentSerializer(serializers.ModelSerializer, ReprMixin):
    user = TaggableUserSerializer()
    obj = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ('user', 'created_at', 'comment_text', 'obj')


class TagSerializer(serializers.ModelSerializer):

    user = TaggableUserSerializer()
    class Meta:
        model = Tag
        fields = ('user', 'created_at', 'tag_text',)

class LikeSerializer(serializers.ModelSerializer, ReprMixin):

    user = TaggableUserSerializer()
    obj = serializers.SerializerMethodField()


    class Meta:
        model = Like
        fields = ('user', 'created_at', 'obj',)

class DislikeSerializer(serializers.ModelSerializer):

    user = TaggableUserSerializer()

    class Meta:
        model = Like
        fields = ('user', 'created_at',)

class ReviewSerializer(serializers.ModelSerializer, ReprMixin):
    user = TaggableUserSerializer()
    obj = serializers.SerializerMethodField()
    class Meta:
        model = Review
        fields = ('user', 'review_text', 'rating', 'created_at', 'obj')


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ('url',)


class FollowerSerializer(serializers.ModelSerializer, ReprMixin):

    user = TaggableUserSerializer()
    obj = serializers.SerializerMethodField()

    class Meta:
        model = Follower
        fields = ('user', 'obj',)

class TaggableSerializer(serializers.ModelSerializer):
    """base serializer for all taggable models"""

    id = HashidSerializerCharField()
    recent_likes = LikeSerializer(many=True, read_only=True, required=False)
    recent_dislikes = DislikeSerializer(many=True, required=False)
    recent_comments = CommentSerializer(many=True, required=False)
    recent_reviews = ReviewSerializer(many=True, required=False)
    recent_images = ImageSerializer(many=True, required=False)
    recent_followers = FollowerSerializer(many=True, required=False)
    recent_following = FollowerSerializer(many=True, required=False)


    class Meta:
        model = None
        fields = ['id', 'recent_likes', 'recent_dislikes',
                  'recent_comments', 'recent_reviews', 'recent_followers',
                  'recent_following',
                  'recent_images', 'like_count', 'dislike_count',
                  'comment_count', 'review_count', 'image_count',
                  'follower_count', 'following_count', 'recent_followers',]
