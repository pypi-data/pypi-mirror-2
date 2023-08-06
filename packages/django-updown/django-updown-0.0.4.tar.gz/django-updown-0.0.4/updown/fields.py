# -*- coding: utf-8 -*-
"""
updown.fields
~~~~~~~~~~~~~

Fields needed for the updown ratings

:copyright: 2010, Daniel Banck <dbanck@weluse.de
:license: BSD, see LICENSE for more details.
"""
from django.db.models import IntegerField, PositiveIntegerField
from django.conf import settings

from updown.models import Vote, SCORE_TYPES
from updown.exceptions import InvalidRating, AuthRequired, CannotChangeVote
import updown.forms


if 'django.contrib.contenttypes' not in settings.INSTALLED_APPS:
    raise ImportError("django-updown requires django.contrib.contenttypes in your INSTALLED_APPS")

from django.contrib.contenttypes.models import ContentType

__all__ = ('Rating', 'RatingField',)

try:
    from hashlib import md5
except ImportError:
    from md5 import new as md5

def md5_hexdigest(value):
    return md5(value).hexdigest()


class Rating(object):
    def __init__(self, likes, dislikes):
        self.likes = likes
        self.dislikes = dislikes

class RatingManager(object):
    def __init__(self, instance, field):
        self.content_type = None
        self.instance = instance
        self.field = field

        self.like_field_name = "%s_likes" % (self.field.name,)
        self.dislike_field_name = "%s_dislikes" % (self.field.name,)

    def get_rating_for_user(self, user):
        kwargs = dict(
            content_type = self.get_content_type(),
            object_id = self.instance.pk,
            key = self.field.key
        )

        if not (user and user.is_authenticated()):
            raise AuthRequired("User must be a user, not '%r'" % (user,))

        kwargs['user'] = user

        try:
            rating = Vote.objects.get(**kwargs)
            return rating.score
        except Vote.DoesNotExist:
            pass
        return

    def get_content_type(self):
        if self.content_type is None:
            self.content_type = ContentType.objects.get_for_model(self.instance)
        return self.content_type

    def add(self, score, user, commit=True):
        try:
            score = int(score)
        except (ValueError, TypeError):
            raise InvalidRating("%s is not a valid score for %s" % (score, self.field.name))

        if score not in SCORE_TYPES.values():
            raise InvalidRating("%s is not a valid score" % (score,))

        if user is None or not user.is_authenticated():
            raise AuthRequired("User must be a user, not '%r'" % (user,))

        defaults = dict(
            score = score
        )

        kwargs = dict(
            content_type    = self.get_content_type(),
            object_id       = self.instance.pk,
            key             = self.field.key,
            user            = user,
        )

        try:
            rating, created = Vote.objects.get(**kwargs), False
        except Vote.DoesNotExist:
            kwargs.update(defaults)
            rating, created = Vote.objects.create(**kwargs), True

        has_changed = False
        if not created:
            if self.field.can_change_vote:
                has_changed = True
                if (rating.score == SCORE_TYPES['LIKE']):
                    self.likes -= 1
                else:
                    self.dislikes -= 1
                if (score == SCORE_TYPES['LIKE']):
                    self.likes += 1
                else:
                    self.dislikes += 1
                rating.score = score
                rating.save()
            else:
                raise CannotChangeVote()
        else:
            has_changed = True
            if (rating.score == SCORE_TYPES['LIKE']):
                self.likes += 1
            else:
                self.dislikes += 1

        if has_changed:
            if commit:
                self.instance.save()

    def _get_likes(self, default=None):
        return getattr(self.instance, self.like_field_name, default)

    def _set_likes(self, value):
        return setattr(self.instance, self.like_field_name, value)

    likes = property(_get_likes, _set_likes)

    def _get_dislikes(self, default=None):
        return getattr(self.instance, self.dislike_field_name, default)

    def _set_dislikes(self, value):
        return setattr(self.instance, self.dislike_field_name, value)

    dislikes = property(_get_dislikes, _set_dislikes)

class RatingCreator(object):
    def __init__(self, field):
        self.field = field
        self.like_field_name = "%s_likes" % (self.field.name,)
        self.dislike_field_name = "%s_dislikes" % (self.field.name,)

    def __get__(self, instance, type=None):
        if instance is None:
            return self.field
        return RatingManager(instance, self.field)

    def __set__(self, instance, value):
        if isinstance(value, Rating):
            setattr(instance, self.like_field_name, value.likes)
            setattr(instance, self.dislike_field_name, value.dislikes)
        else:
            raise TypeError("%s value must be a Rating instance, not '%r'" % (self.field.name, value))

class RatingField(IntegerField):
    def __init__(self, delimiter="|", *args, **kwargs):
        self.can_change_vote = kwargs.pop('can_change_vote', False)
        self.delimiter = delimiter
        kwargs['editable'] = False
        kwargs['default'] = 0
        kwargs['blank'] = True
        super(RatingField, self).__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name):
        self.name = name
        self.like_field = PositiveIntegerField(editable=False, default=0, blank=True)
        cls.add_to_class("%s_likes" % (self.name,), self.like_field)
        self.dislike_field = PositiveIntegerField(editable=False, default=0, blank=True)
        cls.add_to_class("%s_dislikes" % (self.name,), self.dislike_field)
        self.key = md5_hexdigest(self.name)

        field = RatingCreator(self)
        if not hasattr(cls, '_ratings'):
            cls._ratings = []
        cls._ratings.append(self)

        setattr(cls, name, field)

    def to_python(self, value):
        # If it's already a list, leave it
        if isinstance(value, list):
            return value

        # Otherwise, split by delimiter
        return value.split(self.delimiter)

    def get_prep_value(self, value):
        return self.delimiter.join(value)

    def get_db_prep_save(self, value):
        pass

    def get_db_prep_lookup(self, lookup_type, value):
        raise NotImplementedError(self.get_db_prep_lookup)

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.RatingField}
        defaults.update(kwargs)
        return super(RatingField, self).formfield(**defaults)

from south.modelsinspector import add_introspection_rules
add_introspection_rules([
    (
        [RatingField], # Class(es) these apply to
        [],         # Positional arguments (not used)
        {           # Keyword argument
            "delimiter": ["delimiter", {"default": "|"}],
        },
    ),
], ["^updown\.fields\.RatingField"])
