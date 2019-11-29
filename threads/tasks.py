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
    comment = Comment.objects.create(
        author=author,
        content=payload["content"],
        thread=thread,
        created_at=datetime.fromisoformat(payload["created_at"]),
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
    thread = Thread.objects.create(title=payload["title"], entity=entity)
    comment = Comment.objects.create(
        author=author,
        content=payload["content"],
        thread=thread,
        created_at=datetime.fromisoformat(payload["created_at"]),
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
