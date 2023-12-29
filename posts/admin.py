from django.contrib import admin

from posts.models import Post, Photo, Like, Hashtag

admin.site.register(Post)
admin.site.register(Photo)
admin.site.register(Like)
admin.site.register(Hashtag)
