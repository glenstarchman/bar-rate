from datetime import datetime, timedelta
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.utils import timezone
from django.utils.functional import cached_property
import pytz
from hashid_field import HashidAutoField
timezone.activate(settings.TIME_ZONE)




class CachedPropertiesMixin():

    def refresh_from_db(self, *args, **kwargs):
        self.invalidate_cached_properties()
        return super().refresh_from_db(*args, **kwargs)

    def invalidate_cached_properties(self):
        for key, value in self.__class__.__dict__.items():
            if isinstance(value, cached_property):
                self.__dict__.pop(key, None)


#ops for soft-deletes
class BarRateDeleteOpsQS(models.QuerySet):
    def delete(self, *args, **kwargs):
        for obj in self:
            obj.delete()

    def undelete(self, *args, **kwargs):
        for obj in self:
            obj.undelete()

    #this may not be needed...
    def update(self, *args, **kwargs):
        for obj in self:
            obj.save()


#the default qs which returns non soft deleted records
class BarRateQuerySet(BarRateDeleteOpsQS):
    def get_queryset(self):
        return self.filter(deleted=False)

    #undelete is a non-op for non soft-deleted objects
    def undelete(self, *args, **kwargs):
        pass


#returns deleted records
class BarRateDeletedQuerySet(BarRateDeleteOpsQS):
    def get_queryset(self):
        return self.filter(deleted=True)

    #delete is a non-op for already soft-deleted objects
    def delete(self, *args, **kwargs):
        pass


#returns ALL objects
class BarRateAllObjectsQuerySet(BarRateDeleteOpsQS):
    def get_queryset(self):
        return self.filter()


class BarRateDeletedManager(models.Manager):
    def get_queryset(self):
        return BarRateDeletedQuerySet(self.model, using=self._db).get_queryset()


class BarRateManager(models.Manager):
    def get_queryset(self):
        return BarRateQuerySet(self.model, using=self._db).get_queryset()


class BarRateAllManager(models.Manager):
    def get_queryset(self):
        return BarRateAllObjectsQuerySet(
            self.model, using=self._db).get_queryset()


class BarRateTimestampModel(models.Model):
    id = HashidAutoField(primary_key=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.created_at is None:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super(BarRateTimestampModel,
              self).save(*args, **kwargs)  # Call the "real" save() method.

    #grab all related fields, except many-to-many
    def all_related(self):
        return [
            f for f in self._meta.get_fields()
            if (f.one_to_many or f.one_to_one) and f.auto_created
            and not f.concrete
        ]

    def _ct(self, obj=None):
        if obj is None: obj = self
        if type(obj) == type(""):
            return ContentType.objects.get_by_natural_key("api", obj)
        else:
            return ContentType.objects.get_for_model(obj)

    #def _get_recent(self, qs, delta=timedelta(days=7)):
    #    if not isinstance(delta, timedelta):
    #        delta = timedelta(days=delta)
    #    return qs.filter(created_at__gte=timezone.now() - delta):5]

    #for pagination
    def _get_recent(self, qs, count=settings.TAGGABLE_COUNT, start=0):
        return list(qs.all()[start:start+count])

    #permissions for dry-rest-permission
    #by default all objects can be read but not written/created
    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    def has_write_permission(request):
        return False

    @staticmethod
    def has_create_permission(request):
        return False

    class Meta:
        abstract = True


class BarRateModel(BarRateTimestampModel, CachedPropertiesMixin):

    #our soft-delete key
    deleted = models.BooleanField(null=False, blank=False, default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    #the default is to return only non-deleted records
    objects = BarRateManager()
    deleted_objects = BarRateDeletedManager()
    all_objects = BarRateAllManager()

    #soft delete this model and all of its relations, except many-to-many
    def delete(self, *args, **kwargs):
        self.deleted = True
        self.deleted_at = timezone.now()
        self.save()

        for rel in self.all_related():
            try:
                f = getattr(self, rel.related_name)
                if hasattr(f, "all"):
                    f.all().delete()
                else:
                    f.delete()
            except:
                pass

    #soft undelete this model and all of its relations, except many-to-many
    def undelete(self, *args, **kwargs):
        self.deleted = False
        self.deleted_at = None
        self.save()
        for rel in self.all_related():
            if hasattr(rel, 'undelete'):
                rel.undelete()
            else:
                f = getattr(self, rel.related_name)
                if hasattr(f, "all"):
                    f.all().undelete()
                else:
                    f.undelete()

    class Meta:
        abstract = True


class BarRateTaggableModel(BarRateModel):

    likes = GenericRelation("Like", related_name="likes")
    dislikes = GenericRelation("Dislike", related_name="dislikes")
    tags = GenericRelation("Tag", related_name="tags")
    comments = GenericRelation("Comment", related_name="comments")
    followers = GenericRelation("Follower", related_name="followers")
    bookmarks = GenericRelation('Bookmark', related_name='bookmarks')
    reviews = GenericRelation('Review', related_name='reviews')
    images = GenericRelation('Image', related_name='images')

    @property
    def followers(self):
        from .taggable import Follower
        ctype = ContentType.objects.get(model='user')
        return Follower.objects.filter(content_type=self._ct(), object_id=self.id)

    @property
    def recent_comments(self, count=settings.TAGGABLE_COUNT, start=0):
        return self._get_recent(self.comments, count, start)

    @property
    def recent_likes(self, count=settings.TAGGABLE_COUNT, start=0):
        return self._get_recent(self.likes, count, start)

    @property
    def recent_dislikes(self, count=settings.TAGGABLE_COUNT, start=0):
        return self._get_recent(self.dislikes, count, start)

    @property
    def recent_followers(self, count=settings.TAGGABLE_COUNT, start=0):
        return self._get_recent(self.followers, count, start)

    @property
    def recent_bookmarks(self, count=settings.TAGGABLE_COUNT, start=0):
        return self._get_recent(self.bookmarks, count, start)

    @property
    def recent_tags(self, count=settings.TAGGABLE_COUNT, start=0):
        return self._get_recent(self.tags, count, start)

    @property
    def recent_reviews(self, count=settings.TAGGABLE_COUNT, start=0):
        return self._get_recent(self.reviews, count, start)

    @property
    def recent_images(self, count=settings.TAGGABLE_COUNT, start=0):
        return self._get_recent(self.images, count, start)

    @property
    def bookmark_count(self):
        return self.bookmarks.count()

    @property
    def like_count(self):
        return self.likes.count()

    @property
    def dislike_count(self):
        return self.dislikes.count()

    @property
    def comment_count(self):
        return self.comments.count()

    @property
    def follower_count(self):
        return self.followers.count()

    @property
    def following_count(self):
        return self.following.count()

    @property
    def image_count(self):
        return self.images.count()

    @property
    def tag_count(self):
        return self.tags.count()

    @property
    def review_count(self):
        return self.reviews.count()

    def add_dislike(self, user):
        try:
            self.remove_like(user)
            self.dislikes.create(user=user, content_object=self)
        except:
            pass

    def add_like(self, user):
        self.likes.create(
            user=user, content_object=self
        )


    def add_comment(self, user, comment_text):
        self.comments.create(
            user=user, content_object=self, comment_text=comment_text)

    def add_tag(self, user, tag_text):
        self.tags.create(
            user=user, content_object=self, tag_text=tag_text)

    def add_review(self, user, review_text, rating=None):
        self.reviews.create(
            user=user, content_object=self,
            review_text=review_text, rating=rating)

    def add_follower(self, user):
        if self.followers.filter(user=user).count() > 0:
            #unfollow
            self.followers.filter(user=user).delete()
        else:
            self.followers.create(user=user, content_object=self)

    def remove_follower(self, user):
        try:
            id = decode(self.id)
            ct = self._ct()
            self.following.filtert(
                user=user, content_type=ct, object_id=id).delete()
        except:
            pass

    def remove_like(self, user):
        try:
            self.likes.filter(user=user).delete()
        except Exception as e:
            return self.likes

    def remove_dislike(self, user):
        try:
            id = self.id.id
            ct = self._ct()
            self.dislikes.filter(
                user=user).delete()
        except:
            pass

    def add_image(self, user, url):
        self.images.create(user=user, url=url, content_object=self)

    class Meta:
        abstract = True
