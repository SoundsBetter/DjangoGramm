import typing as t

from django.db.models import Model


M = t.TypeVar("M", bound=t.Type[Model])


def directory_path(instance: M, filename: str, base_folder: str) -> str:
    return f"{base_folder}/{instance.id}/{filename}"
