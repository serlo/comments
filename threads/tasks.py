from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from threads.models import Entity, Author, Thread, Comment


def create_comment(payload):
    author, _ = Author.objects.get_or_create(
        user_id=payload["author"]["user_id"],
        provider_id=payload["author"]["provider_id"],
    )
    thread = Thread.objects.get(pk=payload["thread_id"])
    comment = Comment.objects.create(
        author=author, content=payload["content"], thread=thread
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
        author=author, content=payload["content"], thread=thread
    )
    return thread
