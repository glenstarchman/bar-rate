from rest_framework import serializers
from hashid_field.rest import HashidSerializerCharField
from .user import MiniUserSerializer
from ..models.taggable import *


class CommentSerializer(serializers.ModelSerializer):

    user = MiniUserSerializer()
    class Meta:
        model = Comment
        fields = ('user', 'created_at', 'comment_text',)


class TagSerializer(serializers.ModelSerializer):

    user = MiniUserSerializer()
    class Meta:
        model = Tag
        fields = ('user', 'created_at', 'tag_text',)

class LikeSerializer(serializers.ModelSerializer):
    user = MiniUserSerializer()
    class Meta:
        model = Like
        fields = ('user', 'created_at',)

class DislikeSerializer(serializers.ModelSerializer):
    user = MiniUserSerializer()
    class Meta:
        model = Like
        fields = ('user', 'created_at',)

class ReviewSerializer(serializers.ModelSerializer):
    user = MiniUserSerializer()
    class Meta:
        model = Review
        fields = ('user', 'review_text', 'rating', 'created_at',)


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ('url',)


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
