import typing as t

from django.db.models import Model

from posts.settings import PICTURES

M = t.TypeVar("M", bound=t.Type[Model])


def user_directory_path(instance: M, filename: str) -> str:
    return f"{PICTURES}/{instance.post.user.id}/{filename}"
