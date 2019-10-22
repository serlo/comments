from django.db import models

# Create your models here.


class Entity(models.Model):
    entity_id = models.CharField(max_length=200)
    platform_id = models.CharField(max_length=200)


class Thread(models.Model):
    title = models.CharField(max_length=200)
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)


class Author(models.Model):
    user_id = models.CharField(max_length=200)
    platform_id = models.CharField(max_length=200)


class Comment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
