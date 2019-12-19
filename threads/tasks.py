from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from threads.models import Entity, Author, Thread, Comment
from datetime import datetime


def create_comment(payload):
    author, _ = Author.objects.get_or_create(
        user_id=payload["author"]["user_id"],
        provider_id=payload["author"]["provider_id"],
    )
    thread = Thread.objects.get(pk=payload["thread_id"])
    thread.updated_at = payload["created_at"]
    comment = Comment.objects.create(
        author=author,
        content=payload["content"],
        thread=thread,
        created_at=datetime.fromisoformat(payload["created_at"]),
        updated_at=datetime.fromisoformat(payload["created_at"]),
    )
    return comment


def create_thread(payload):
    author, _ = Author.objects.get_or_create(
        user_id=payload["author"]["user_id"],
        provider_id=payload["author"]["provider_id"],
    )
    entity, _ = Entity.objects.get_or_create(
        entity_id=payload["entity"]["id"], provider_id=payload["entity"]["provider_id"]
    )
    thread = Thread.objects.create(
        title=payload["title"],
        entity=entity,
        created_at=payload["created_at"],
        updated_at=payload["created_at"],
    )
    comment = Comment.objects.create(
        author=author,
        content=payload["content"],
        thread=thread,
        created_at=datetime.fromisoformat(payload["created_at"]),
        updated_at=datetime.fromisoformat(payload["created_at"]),
    )
    return thread


def delete_thread(payload):
    thread_found = Thread.objects.get(pk=payload["thread_id"])
    thread_found.delete()


def delete_comment(payload):
    comment_found = Comment.objects.get(pk=payload["comment_id"])
    comment_found.delete()


def archive_thread(payload):
    thread_found = Thread.objects.get(pk=payload["thread_id"])
    thread_found.archived = True
    thread_found.save()
    return thread_found


def unarchive_thread(payload):
    thread_found = Thread.objects.get(pk=payload["thread_id"])
    thread_found.archived = False
    thread_found.save()
    return thread_found


def edit_comment(payload):
    comment_found = Comment.objects.get(pk=payload["comment_id"])
    comment_found.content = payload["content"]
    comment_found.updated_at = payload["created_at"]
    comment_found.thread.updated_at = payload["created_at"]
    comment_found.save()
    return comment_found


def trash_thread(payload):
    thread_found = Thread.objects.get(pk=payload["thread_id"])
    thread_found.trashed = True
    thread_found.save()
    return thread_found


def restore_thread(payload):
    thread_found = Thread.objects.get(pk=payload["thread_id"])
    thread_found.trashed = False
    thread_found.save()
    return thread_found


def trash_comment(payload):
    comment_found = Comment.objects.get(pk=payload["comment_id"])
    comment_found.trashed = True
    comment_found.save()
    return comment_found


def restore_comment(payload):
    comment_found = Comment.objects.get(pk=payload["comment_id"])
    comment_found.trashed = False
    comment_found.save()
    return comment_found


def replace_user(payload):
    author_found = Author.objects.get(user_id=payload["anonymous_id"])
    author_found.user_id = payload["user_id"]
    return author_found
