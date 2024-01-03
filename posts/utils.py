import typing as t
from itertools import chain

from django.db.models import Model

from posts.models import Hashtag

M = t.TypeVar("M", bound=Model)


def hashtag_handler(post: M, hashtags: list[str]) -> None:
    existing_hashtags = Hashtag.objects.filter(name__in=hashtags)
    existing_hashtag_names = (hashtag.name for hashtag in existing_hashtags)
    new_hashtags = [
        Hashtag(name=name)
        for name in hashtags
        if name not in existing_hashtag_names
    ]
    Hashtag.objects.bulk_create(new_hashtags)
    for hashtag in chain(existing_hashtags, new_hashtags):
        post.hashtags.add(hashtag)
