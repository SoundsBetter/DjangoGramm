import typing as t

from django.db.models import Model


M = t.TypeVar("M", bound=Model)


def directory_path(instance: M, filename: str, base_folder: str) -> str:
    if hasattr(instance, "post"):
        return f"{base_folder}/post_id_{instance.post.pk}/{filename}"
    else:
        return f"{base_folder}/user_id_{instance.pk}/{filename}"
