import typing as t

from django.db.models import Model

from posts.models import Hashtag

M = t.TypeVar("M", bound=t.Type[Model])


def hashtag_handler(post: M, hashtags: list[str]) -> None:
    existing_hashtags = [hashtag.name for hashtag in Hashtag.objects.all()]
    for hashtag_text in hashtags:
        if hashtag_text not in existing_hashtags:
            hashtag = Hashtag.objects.create(name=hashtag_text)
            post.hashtags.add(hashtag)
