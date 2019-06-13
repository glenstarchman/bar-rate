import string
import random
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.db.models.signals import (pre_save, post_save)
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from django.apps import apps
from hashid_field import Hashid
from rest_framework.authtoken.models import Token
from .base import *
from .taggable import *
from ..util.exceptions import BarRateValidationException
from dry_rest_permissions.generics import allow_staff_or_superuser, authenticated_users, unauthenticated_users


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """make sure the user has a token and a username"""
    if created:
        Token.objects.create(user=instance)
        from .profile import Profile
        #create a blank profile
        p = Profile(user=instance)
        p.save()
        #create a blank user_settings
        from .user_settings import UserSetting
        us = UserSetting(user=instance)
        us.save()




@receiver(pre_save, sender=settings.AUTH_USER_MODEL)
def create_username(sender, instance=None, created=False, **kwargs):
    if not instance.username:
        hint = "%s.%s" % (instance.first_name, instance.last_name)
        username = User.objects.generate_unique_username(hint)
        instance.username = username


class UserBase(AbstractBaseUser, PermissionsMixin):
    class Meta:
        abstract = True


class CustomUserManager(BaseUserManager, BarRateManager):
    def __contains(self, s, comp):
        """ Check whether sequence str contains ANY of the items in set. """
        return 1 in [c in s for c in comp]

    def validate_username(self, username):
        """check if a username is unique"""
        if self.filter(username__iexact=username).count() == 0:
            if len(username) < 4:
                return ["Username must be at least 4 characters"]
            return []
        else:
            return ["Username is not unique"]

    def validate_email(self, email):
        """check if an email is unique"""
        if self.filter(email__iexact=email).count() == 0:
            return []

    def validate_password(self, password):
        """make sure a password meets requirements"""
        errors = []

        if len(password) < 8:
            errors.append("Password must be at least 8 characters long")

        #check for at least one special character
        #s = list(settings.SPECIAL_CHARS)
        #if not self.__contains(password, s):
        #    errors.append("Password must contain one of: %s" % (', '.join(s)))

        ##check for at least one digit
        #if not self.__contains(password, list(settings.NUMBERS)):
        #    errors.append("Password must contain at least one digit")

        return errors

    def generate_unique_username(self, hint=''):
        #check if 'hint' is already used... this is first.last
        hint = hint.lower()
        if self.filter(username__iexact=hint).count() == 0:
            #this is unique so use it
            return hint
        else:
            users = User.objects.filter(username__regex=r'^%s[1-9]{1,}$' % (
                hint)).order_by('username').values('username')
            if len(users) > 0:
                last_number_used = map(
                    lambda x: int(x['username'].replace(hint, '')), users)
                last_number_used.sort()
                last_number_used = last_number_used[-1]
                number = last_number_used + 1
                username = hint
            else:
                username = '%s%s' % (hint, 1)

        return username

    def _create_user(self, email, password, is_staff, is_superuser,
                     **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)


class User(UserBase, BarRateTaggableModel):

    id = HashidAutoField(allow_int_lookup=True, primary_key=True)
    username = models.CharField(_('user name'), max_length=254, unique=True)
    email = models.EmailField(_('email address'), max_length=254, unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    @staticmethod
    def add_reset_token(email):
        """add a reset token to a given user"""
        try:
            user = User.objects.get(email__iexact=email)
            code = ''.join([random.choice(string.digits) for n in range(6)])
            user.reset_token = code
            user.save()
        except Exception as e:
            pass


    @staticmethod
    def get_by_reset_token(email, token):
        try:
            return User.objects.get(email=email, reset_token=token)
        except Exception as e:
            return None

    @staticmethod
    def apply_reset_token(email, token, new_password):
        user = User.get_by_reset_token(email, token)
        if user:
            user.set_password(new_password)
            user.save()

    def __repr__(self):
        return "%s %s" % (self.first_name, self.last_name)

    def __str__(self):
        if self.first_name:
            return "%s %s" % (self.first_name, self.last_name)
        else:
            return self.username


    @staticmethod
    @allow_staff_or_superuser
    @unauthenticated_users
    def has_create_permission(request):
        return True

    @authenticated_users
    def has_write_permission(request):
        if request.user.is_superuser() or request.user.id == self.id:
            return True
        else:
            return False

    def set_password(self, password):
        if not password: return []
        errors = User.objects.validate_password(password)
        if len(errors) > 0:
            raise BarRateValidationException(errors=errors)
        super(User,
              self).set_password(password)  # Call the "real" save() method.

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def __get_bookmarks(self, bookmark_type):
        ct = ContentType.objects.get_for_model(bookmark_type)
        return Bookmark.objects.filter(
            user=self, content_type=ct).order_by("-created_at")

    def bookmarks(self, bookmark_type="all"):
        from .get_taggable import TAGGABLE_MODEL_NAMES
        if bookmark_type == "all":
            #special case to return all bookmarks regardless of type
            return Bookmark.objects.filter(user=self)
        else:
            if type(bookmark_type) != type("") and issubclass(
                    bookmark_type, BarRateTaggableModel):
                return self.__get_bookmarks(bookmark_type)
            else:
                #need to look it up by name
                bt = bookmark_type.lower()
                if bt in TAGGABLE_MODEL_NAMES:
                    model = apps.get_model('api', bt)
                    return self.__get_bookmarks(model)
                else:
                    return []

    def add_bookmark(self, obj):
        try:
            ct = ContentType.objects.get_for_model(obj)
            bm = Bookmark.objects.get(
                user=self, content_type=ct, object_id=obj.id)
        except Exception as e:
            b = Bookmark.objects.create(user=self, content_object=obj)
            b.save()
            return b

    def __sort(self, qs):
        return qs.order_by("-created_at")


    def add_like(self, obj):
        id = Hashid(obj.id).id
        ct = obj._ct()
        qs = Like.objects.filter(user=self, content_type=ct, object_id=id)
        if qs.count() > 0:
            qs.delete()
        else:
            like = Like(user=self, content_type=ct, object_id=id)
            like.save()


    @property
    def settings(self):
        return self.usersetting_set.first()

    @property
    def user_likes(self):
        """retrieve a list of all likes OF of this user"""
        return self.__sort(Like.objects.filter(user=self))

    @property
    def user_likes_count(self):
        return Like.objects.filter(user=self).count()

    @property
    def user_dislikes(self):
        """retrieve a list of all dislikes OF this user"""
        return self.__sort(Dislike.objects.filter(user=self))

    @property
    def user_dislikes_count(self):
        return Dislike.objects.filter(user=self).count()

    @property
    def user_following(self):
        """get a list of all people this user is FOLLOWING"""
        return self.__sort(Follower.objects.filter(user=self))

    @property
    def user_following_count(self):
        return Follower.objects.filter(user=self).count()

    @property
    def user_comments(self):
        """retrieve a list of all comments BY this user"""
        return self.__sort(Comment.objects.filter(user=self))

    @property
    def user_comments_count(self):
        return Comment.objects.filter(user=self).count()


    @property
    def user_reviews(self):
        return Review.objects.filter(user=self)


    @property
    def current_checkin(self):
        from .bar import BarCheckin
        now = timezone.now()
        long_time = now - timedelta(hours=4)

        try:
            qs = BarCheckin.objects.get(
                Q(user=self) &
                (Q(created_at__gte=long_time) & Q(checkout__isnull=True))
            )
            return qs
        except Exception as e:
            return None

    @property
    def recent_user_likes(self, days=7):
        return self._get_recent(self.user_likes, days)

    @property
    def recent_user_dislikes(self, days=7):
        return self._get_recent(self.user_dislikes, days)

    @property
    def recent_user_following(self, days=7):
        return self._get_recent(self.user_following, days)

    @property
    def recent_user_comments(self, days=7):
        return self._get_recent(self.user_comments, days)

    def mutual_followers(self, user_id):
        """get the mutual followers between two users"""
        pass


    @property
    def recent_user_reviews(self, days=7):
        return self._get_recent(self.user_reviews, days)

    def mutual_followers_count(self, user_id):
        return self.mutual_followers(user_id).count()

    def is_followed_by(self, user_id):
        """is this user followed by the other user?"""
        pass

    def suggested_followers(self, user_id):
        """suggest others to follow from other user's followers"""
        pass

    def mutual_likes(self, user_id):
        """return a list of mutual likes between two users"""
        pass

    def mutual_likes_count(self, user_id):
        return self.mutual_likes(user_id).count()

    def mutual_dislikes(self, user_id):
        """return a list of mutual dislikes between two users"""
        pass

    def mutual_dislikes_count(self, user_id):
        return self.mutual_dislikes(user_id).count()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = "users"
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['username']),
            models.Index(fields=['first_name']),
            models.Index(fields=['last_name']),
        ]

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.email)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])

    def get_profile(self):
        from .profile import Profile
        return Profile.objects.get_or_create(user_id=self)[0]

    #USERNAME_FIELD = 'email'
