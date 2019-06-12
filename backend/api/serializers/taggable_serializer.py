from rest_framework import serializers
from hashid_field.rest import HashidSerializerCharField
from ..models.user import User
from ..models.taggable import *


class TaggableUserSerializer(serializers.ModelSerializer):
    id = HashidSerializerCharField()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username',)


class CommentSerializer(serializers.ModelSerializer):

    user = TaggableUserSerializer()
    class Meta:
        model = Comment
        fields = ('user', 'created_at', 'comment_text',)


class TagSerializer(serializers.ModelSerializer):

    user = TaggableUserSerializer()
    class Meta:
        model = Tag
        fields = ('user', 'created_at', 'tag_text',)

class LikeSerializer(serializers.ModelSerializer):
    user = TaggableUserSerializer()
    class Meta:
        model = Like
        fields = ('user', 'created_at',)

class DislikeSerializer(serializers.ModelSerializer):

    user = TaggableUserSerializer()

    class Meta:
        model = Like
        fields = ('user', 'created_at',)

class ReviewSerializer(serializers.ModelSerializer):
    user = TaggableUserSerializer()
    class Meta:
        model = Review
        fields = ('user', 'review_text', 'rating', 'created_at',)


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ('url',)


class FollowerSerializer(serializers.ModelSerializer):

    user = TaggableUserSerializer()

    class Meta:
        model = Follower
        fields = ('user',)

class TaggableSerializer(serializers.ModelSerializer):
    """base serializer for all taggable models"""

    id = HashidSerializerCharField()
    recent_likes = LikeSerializer(many=True, read_only=True, required=False)
    recent_dislikes = DislikeSerializer(many=True, required=False)
    recent_comments = CommentSerializer(many=True, required=False)
    recent_reviews = ReviewSerializer(many=True, required=False)
    recent_images = ImageSerializer(many=True, required=False)

    class Meta:
        model = None
        fields = ['id', 'recent_likes', 'recent_dislikes',
                  'recent_comments', 'recent_reviews',
                  'recent_images', 'like_count', 'dislike_count',
                  'comment_count', 'review_count', 'image_count',]
