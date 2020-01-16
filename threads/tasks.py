from threads.models import Entity, Author, Thread, Comment
from datetime import datetime
from typing import TypedDict


class AuthorPayload(TypedDict):
    provider_id: str
    user_id: str


class EntityPayload(TypedDict):
    provider_id: str
    id: str


class CreateCommentPayload(TypedDict):
    author: AuthorPayload
    thread_id: str
    created_at: str
    content: str


def create_comment(payload: CreateCommentPayload) -> Comment:
    author = get_author_or_create(payload["author"])
    thread = Thread.objects.get(pk=payload["thread_id"])
    thread.updated_at = datetime_from_timestamp(payload["created_at"])
    comment = Comment.objects.create(
        author=author,
        content=payload["content"],
        thread=thread,
        created_at=datetime_from_timestamp(payload["created_at"]),
        updated_at=datetime_from_timestamp(payload["created_at"]),
    )
    return comment


class CreateThreadPayload(TypedDict):
    author: AuthorPayload
    entity: EntityPayload
    title: str
    content: str
    created_at: str


def create_thread(payload: CreateThreadPayload) -> Thread:
    author = get_author_or_create(payload["author"])
    entity, _ = Entity.objects.get_or_create(
        entity_id=payload["entity"]["id"], provider_id=payload["entity"]["provider_id"]
    )
    thread = Thread.objects.create(
        title=payload["title"],
        entity=entity,
        created_at=datetime_from_timestamp(payload["created_at"]),
        updated_at=datetime_from_timestamp(payload["created_at"]),
    )
    Comment.objects.create(
        author=author,
        content=payload["content"],
        thread=thread,
        created_at=datetime_from_timestamp(payload["created_at"]),
        updated_at=datetime_from_timestamp(payload["created_at"]),
    )
    return thread


class DeleteThreadPayload(TypedDict):
    thread_id: str


def delete_thread(payload: DeleteThreadPayload) -> None:
    thread_found = Thread.objects.get(pk=payload["thread_id"])
    thread_found.delete()


class DeleteCommentPayload(TypedDict):
    comment_id: str


def delete_comment(payload: DeleteCommentPayload) -> None:
    comment_found = Comment.objects.get(pk=payload["comment_id"])
    comment_found.delete()


class ArchiveThreadPayload(TypedDict):
    thread_id: str


def archive_thread(payload: ArchiveThreadPayload) -> Thread:
    thread_found = Thread.objects.get(pk=payload["thread_id"])
    thread_found.archived = True
    thread_found.save()
    return thread_found


class UnarchiveThreadPayload(TypedDict):
    thread_id: str


def unarchive_thread(payload: UnarchiveThreadPayload) -> Thread:
    thread_found = Thread.objects.get(pk=payload["thread_id"])
    thread_found.archived = False
    thread_found.save()
    return thread_found


class EditCommentPayload(TypedDict):
    comment_id: str
    content: str
    created_at: str


def edit_comment(payload: EditCommentPayload) -> Comment:
    comment_found = Comment.objects.get(pk=payload["comment_id"])
    comment_found.content = payload["content"]
    comment_found.updated_at = datetime_from_timestamp(payload["created_at"])
    comment_found.save()
    comment_found.thread.updated_at = datetime_from_timestamp(payload["created_at"])
    comment_found.thread.save()
    return comment_found


class TrashThreadPayload(TypedDict):
    thread_id: str


def trash_thread(payload: TrashThreadPayload) -> Thread:
    thread_found = Thread.objects.get(pk=payload["thread_id"])
    thread_found.trashed = True
    thread_found.save()
    return thread_found


class RestoreThreadPayload(TypedDict):
    thread_id: str


def restore_thread(payload: RestoreThreadPayload) -> Thread:
    thread_found = Thread.objects.get(pk=payload["thread_id"])
    thread_found.trashed = False
    thread_found.save()
    return thread_found


class TrashCommentPayload(TypedDict):
    comment_id: str


def trash_comment(payload: TrashCommentPayload) -> Comment:
    comment_found = Comment.objects.get(pk=payload["comment_id"])
    comment_found.trashed = True
    comment_found.save()
    return comment_found


class RestoreCommentPayload(TypedDict):
    comment_id: str


def restore_comment(payload: RestoreCommentPayload) -> Comment:
    comment_found = Comment.objects.get(pk=payload["comment_id"])
    comment_found.trashed = False
    comment_found.save()
    return comment_found


class ReplaceUserPayload(TypedDict):
    old: AuthorPayload
    new: AuthorPayload


def replace_user(payload: ReplaceUserPayload) -> Author:
    author = Author.objects.get(**payload["old"])
    author.provider_id = payload["new"]["provider_id"]
    author.user_id = payload["new"]["user_id"]
    author.save()
    return author


def get_author_or_create(payload: AuthorPayload) -> Author:
    author, _ = Author.objects.get_or_create(
        user_id=payload["user_id"], provider_id=payload["provider_id"],
    )
    return author


def datetime_from_timestamp(timestamp: str) -> datetime:
    return datetime.fromisoformat(timestamp)
