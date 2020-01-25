from threads.models import Entity, User, Thread, Comment, UserReport, Subscription
from datetime import datetime
from typing import TypedDict


class UserPayload(TypedDict):
    provider_id: str
    user_id: str


class EntityPayload(TypedDict):
    provider_id: str
    id: str


class CreateThreadPayload(TypedDict):
    user: UserPayload
    entity: EntityPayload
    title: str
    content: str
    created_at: str


def create_thread(payload: CreateThreadPayload) -> Thread:
    user = get_user_or_create(payload["user"])
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
        user=user,
        content=payload["content"],
        thread=thread,
        created_at=datetime_from_timestamp(payload["created_at"]),
        updated_at=datetime_from_timestamp(payload["created_at"]),
    )
    get_subscription_or_create(user, thread)
    return thread


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


class DeleteThreadPayload(TypedDict):
    thread_id: str


def delete_thread(payload: DeleteThreadPayload) -> None:
    thread_found = Thread.objects.get(pk=payload["thread_id"])
    thread_found.delete()


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


class CreateCommentPayload(TypedDict):
    user: UserPayload
    thread_id: str
    created_at: str
    content: str


def create_comment(payload: CreateCommentPayload) -> Comment:
    user = get_user_or_create(payload["user"])
    thread = Thread.objects.get(pk=payload["thread_id"])
    thread.updated_at = datetime_from_timestamp(payload["created_at"])
    comment = Comment.objects.create(
        user=user,
        content=payload["content"],
        thread=thread,
        created_at=datetime_from_timestamp(payload["created_at"]),
        updated_at=datetime_from_timestamp(payload["created_at"]),
    )
    get_subscription_or_create(user, thread)
    return comment


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


class DeleteCommentPayload(TypedDict):
    comment_id: str


def delete_comment(payload: DeleteCommentPayload) -> None:
    comment_found = Comment.objects.get(pk=payload["comment_id"])
    comment_found.delete()


class CreateUserReportPayload(TypedDict):
    user: UserPayload
    thread_id: str
    comment_id: str
    created_at: str
    description: str
    category: str


def create_user_report(payload: CreateUserReportPayload) -> UserReport:
    user = get_user_or_create(payload["user"])
    thread = Thread.objects.get(pk=payload["thread_id"])
    comment = (
        Comment.objects.get(pk=payload["comment_id"]) if payload["comment_id"] else None
    )
    user_report = UserReport.objects.create(
        description=payload["description"],
        category=payload["category"],
        user=user,
        thread=thread,
        comment=comment,
        created_at=datetime_from_timestamp(payload["created_at"]),
    )
    return user_report


class DeleteUserReportPayload(TypedDict):
    user_report_id: str


def delete_user_report(payload: DeleteUserReportPayload) -> None:
    user_report_found = UserReport.objects.get(pk=payload["user_report_id"])
    user_report_found.delete()


class ReplaceUserPayload(TypedDict):
    old: UserPayload
    new: UserPayload


def replace_user(payload: ReplaceUserPayload) -> User:
    user = User.objects.get(**payload["old"])
    user.provider_id = payload["new"]["provider_id"]
    user.user_id = payload["new"]["user_id"]
    user.save()
    return user


class CreateSubscriptionPayload(TypedDict):
    user: UserPayload
    thread_id: str


def create_subscription(payload: CreateSubscriptionPayload) -> Subscription:
    user = get_user_or_create(payload["user"])
    thread = Thread.objects.get(pk=payload["thread_id"])
    return get_subscription_or_create(user, thread)


class DeleteSubscriptionPayload(TypedDict):
    subscription_id: str


def delete_subscription(payload: DeleteSubscriptionPayload) -> None:
    subscription_found = Subscription.objects.get(pk=payload["subscription_id"])
    subscription_found.delete()


def get_user_or_create(payload: UserPayload) -> User:
    user, _ = User.objects.get_or_create(
        user_id=payload["user_id"], provider_id=payload["provider_id"],
    )
    return user


def get_subscription_or_create(user: User, thread: Thread) -> Subscription:
    subscription, _ = Subscription.objects.get_or_create(user=user, thread=thread)
    return subscription


def datetime_from_timestamp(timestamp: str) -> datetime:
    return datetime.fromisoformat(timestamp)
