from django.db import models
import uuid

# Create your models here.


class Entity(models.Model):
    entity_id = models.CharField(max_length=200)
    provider_id = models.CharField(max_length=200)


class Thread(models.Model):
    title = models.CharField(max_length=200)
    archived = models.BooleanField(default=False)
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "comments": [comment.to_json() for comment in self.comment_set.all()],
        }


class Author(models.Model):
    user_id = models.CharField(max_length=200)
    provider_id = models.CharField(max_length=200)

    def to_json(self):
        return {"provider_id": self.provider_id, "user_id": self.user_id}


class Comment(models.Model):
    created_at = models.DateTimeField()
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def to_json(self):
        return {
            "id": self.id,
            "content": self.content,
            "created_at": self.created_at.isoformat(timespec="seconds"),
            "author": self.author.to_json(),
        }
