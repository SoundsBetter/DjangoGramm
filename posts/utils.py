import typing as t
from itertools import chain

from django.db import IntegrityError
from django.db.models import Model

from posts.models import Hashtag

M = t.TypeVar("M", bound=Model)


def hashtag_handler(post: M, hashtags: list[str]) -> None:
    existing_hashtags = Hashtag.objects.filter(name__in=hashtags)
    _new_names = set(hashtags) - set(
        hashtag.name for hashtag in existing_hashtags
    )
    if _new_names:
        new_hashtags = [Hashtag(name=name) for name in _new_names]
        try:
            Hashtag.objects.bulk_create(new_hashtags)
        except IntegrityError:
            pass
        post.hashtags.add(*new_hashtags)
    post.hashtags.add(*existing_hashtags)
