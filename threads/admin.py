from django.contrib import admin

from .models import Comment, Thread, Author, Entity

# Register your models here.

admin.site.register(Comment)
admin.site.register(Author)
admin.site.register(Entity)
admin.site.register(Thread)
