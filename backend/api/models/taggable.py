from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from .base import *


class Taggable(BarRateTimestampModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __repr__(self):
        return "<%s: %s (%s)>" % (self.__class__.__name__, self.content_type.name, self.object_id,)

    class Meta:
        abstract = True


class Like(Taggable):

    class Meta:
        db_table = "like"
        indexes = [
            models.Index(fields = ['object_id']),
            models.Index(fields = ['created_at']),
        ]

        unique_together = ['user', 'content_type', 'object_id']
        ordering = ["-created_at"]

class Dislike(Taggable):

    class Meta:
        db_table = "dislike"
        indexes = [
            models.Index(fields = ['object_id']),
            models.Index(fields = ['created_at']),
        ]
        unique_together = ['user', 'content_type', 'object_id']
        ordering = ["-created_at"]

class Comment(Taggable):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    comment_text = models.TextField()

    class Meta:
        db_table = "comment"
        indexes = [
            models.Index(fields = ['object_id']),
            models.Index(fields = ['created_at']),
        ]
        ordering = ["-created_at"]

class Tag(Taggable):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    tag_text = models.TextField()

    class Meta:
        db_table = "tag"
        indexes = [
            models.Index(fields = ['object_id']),
            models.Index(fields = ['created_at']),
        ]
        ordering = ["-created_at"]


class Follower(Taggable):

    class Meta:
        db_table = "follower"
        indexes = [
            models.Index(fields = ['object_id']),
            models.Index(fields = ['created_at']),
        ]

        unique_together = ['user', 'content_type', 'object_id']
        ordering = ["-created_at"]

class Image(Taggable):

    url = models.CharField(max_length = 1024)
    class Meta:
        db_table = "image"
        indexes = [
            models.Index(fields = ['object_id']),
            models.Index(fields = ['created_at']),
        ]
        ordering = ["-created_at"]

class Bookmark(Taggable):

    class Meta:
        db_table = "bookmark"
        indexes = [
            models.Index(fields = ['object_id']),
            models.Index(fields = ['created_at']),
        ]

        unique_together = ['user', 'content_type', 'object_id']
        ordering = ["-created_at"]

class Review(Taggable):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    review_text = models.TextField()
    rating = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        db_table = "review"
        indexes = [
            models.Index(fields = ['object_id']),
            models.Index(fields = ['created_at']),
        ]
        ordering = ["-created_at"]
