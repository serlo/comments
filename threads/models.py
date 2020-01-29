from django.db import models
from typing import List, TypedDict
import uuid


class UserJson(TypedDict):
    provider_id: str
    id: str


class CommentJson(TypedDict):
    id: uuid.UUID
    content: str
    created_at: str
    updated_at: str
    user: UserJson


class ThreadJson(TypedDict):
    id: uuid.UUID
    title: str
    created_at: str
    updated_at: str
    comments: List[CommentJson]


class UserReportJson(TypedDict):
    id: uuid.UUID
    created_at: str
    description: str
    category: str
    user: UserJson
    thread: ThreadJson
    comment: CommentJson


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


class User(models.Model):
    user_id = models.CharField(max_length=200)
    provider_id = models.CharField(max_length=200)

    def to_json(self) -> UserJson:
        return {"provider_id": self.provider_id, "id": self.user_id}


class Comment(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    content = models.TextField()
    trashed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def to_json(self) -> CommentJson:
        return {
            "id": self.id,
            "content": self.content,
            "created_at": self.created_at.isoformat(timespec="seconds"),
            "updated_at": self.updated_at.isoformat(timespec="seconds"),
            "user": self.user.to_json(),
        }


class UserReport(models.Model):
    created_at = models.DateTimeField()
    description = models.TextField()
    category = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, blank=True, null=True
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def to_json(self) -> UserReportJson:
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(timespec="seconds"),
            "description": self.description,
            "category": self.category,
            "user": self.user.to_json(),
            "thread": self.thread.to_json(),
            "comment": self.comment.to_json(),
        }
