from django.contrib import admin

from posts.models import (
    Post,
    Photo,
    Like,
    Hashtag,
    Comment,
)

admin.site.register(Post)
admin.site.register(Photo)
admin.site.register(Like)
admin.site.register(Hashtag)
admin.site.register(Comment)
