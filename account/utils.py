from account.settings import AVATARS


def user_directory_path(instance, filename: str) -> str:
    return f"{AVATARS}/{instance.user.id}/{filename}"
