from django.contrib import admin

from .models import Post, User

admin.site.register(Post)
# admin.site.register(UserProfile)
admin.site.register(User)

