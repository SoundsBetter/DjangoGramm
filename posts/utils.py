from posts.settings import PICTURES


def user_directory_path(instance, filename: str) -> str:
    return f"{PICTURES}/{instance.post.user.id}/{filename}"
