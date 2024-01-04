import typing as t
from itertools import chain

from django.db.models import Model

from posts.models import Hashtag

M = t.TypeVar("M", bound=Model)

"""
Вирішив залишити другий варіант, так як хештегів не має бути дуже багато (хоча
якщо користувачів мільйони то вже питання), а функція виходить набагато простіша
і зрозуміліша. В першому варіанті зробив ignore_conflicts=True, тому що False 
йде по дефолту і викликає IntegrityError якщо раптом станеться помилка і функція
таки спробує додати хештег повторно. Я розумію, що достатньо просто залишити 
існуючий екземпляр, тому додав gnore_conflicts=True  
"""

# def hashtag_handler(post: M, hashtags: list[str]) -> None:
#     existing_hashtags = Hashtag.objects.filter(name__in=hashtags)
#     _new_names = set(hashtags) - set(
#         hashtag.name for hashtag in existing_hashtags
#     )
#     if _new_names:
#         new_hashtags = [Hashtag(name=name) for name in _new_names]
#         Hashtag.objects.bulk_create(new_hashtags, ignore_conflicts=True)
#         post.hashtags.add(*new_hashtags)
#     post.hashtags.add(*existing_hashtags)


def hashtag_handler(post: M, hashtags: list[str]) -> None:
    _hashtags = [
        Hashtag.objects.get_or_create(name=name)[0] for name in hashtags
    ]
    post.hashtags.add(*_hashtags)
