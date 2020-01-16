from django.db import models
from typing import List, TypedDict
import uuid


class AuthorJson(TypedDict):
    provider_id: str
    user_id: str


class CommentJson(TypedDict):
    id: uuid.UUID
    content: str
    created_at: str
    updated_at: str
    author: AuthorJson


class ThreadJson(TypedDict):
    id: uuid.UUID
    title: str
    created_at: str
    updated_at: str
    comments: List[CommentJson]


class Entity(models.Model):
    entity_id = models.CharField(max_length=200)
    provider_id = models.CharField(max_length=200)


class Thread(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    title = models.CharField(max_length=200)
    archived = models.BooleanField(default=False)
    trashed = models.BooleanField(default=False)
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def to_json(self) -> ThreadJson:
        return {
            "id": self.id,
            "title": self.title,
            "comments": [comment.to_json() for comment in self.comment_set.all()],
            "created_at": self.created_at.isoformat(timespec="seconds"),
            "updated_at": self.updated_at.isoformat(timespec="seconds"),
        }


class Author(models.Model):
    user_id = models.CharField(max_length=200)
    provider_id = models.CharField(max_length=200)

    def to_json(self) -> AuthorJson:
        return {"provider_id": self.provider_id, "user_id": self.user_id}


class Comment(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    content = models.TextField()
    trashed = models.BooleanField(default=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def to_json(self) -> CommentJson:
        return {
            "id": self.id,
            "content": self.content,
            "author": self.author.to_json(),
            "created_at": self.created_at.isoformat(timespec="seconds"),
            "updated_at": self.updated_at.isoformat(timespec="seconds"),
        }
