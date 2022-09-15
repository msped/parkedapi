from django.contrib import admin

from .models import Post, PostLikes, Comment, CommentLikes

# Register your models here.

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(PostLikes)
admin.site.register(CommentLikes)
