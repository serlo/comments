from django.contrib import admin

from .models import Comment, Thread, User, Entity, UserReport

# Register your models here.

admin.site.register(Comment)
admin.site.register(User)
admin.site.register(Entity)
admin.site.register(Thread)
admin.site.register(UserReport)
