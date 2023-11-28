from typing import TypeVar

from django.db.models import Model

from account.settings import AVATARS

M = TypeVar("M", bound=Model)


def user_directory_path(instance: M, filename: str) -> str:
    return f"{AVATARS}/{instance.user.id}/{filename}"
