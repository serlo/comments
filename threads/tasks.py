from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from threads.models import Entity, User, Thread, Comment, UserReport
from datetime import datetime


def create_comment(payload):
    user, _ = User.objects.get_or_create(
        user_id=payload["user"]["user_id"], provider_id=payload["user"]["provider_id"],
    )
    thread = Thread.objects.get(pk=payload["thread_id"])
    comment = Comment.objects.create(
        user=user,
        content=payload["content"],
        thread=thread,
        created_at=datetime.fromisoformat(payload["created_at"]),
    )
    return comment


def create_thread(payload):
    user, _ = User.objects.get_or_create(
        user_id=payload["user"]["user_id"], provider_id=payload["user"]["provider_id"],
    )
    entity, _ = Entity.objects.get_or_create(
        entity_id=payload["entity"]["id"], provider_id=payload["entity"]["provider_id"]
    )
    thread = Thread.objects.create(title=payload["title"], entity=entity)
    comment = Comment.objects.create(
        user=user,
        content=payload["content"],
        thread=thread,
        created_at=datetime.fromisoformat(payload["created_at"]),
    )
    return thread


def create_user_report(payload):
    user, _ = User.objects.get_or_create(
        user_id=payload["user"]["user_id"], provider_id=payload["user"]["provider_id"],
    )
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
        created_at=datetime.fromisoformat(payload["created_at"]),
    )
    return user_report


def delete_thread(payload):
    thread_found = Thread.objects.get(pk=payload["thread_id"])
    thread_found.delete()


def delete_comment(payload):
    comment_found = Comment.objects.get(pk=payload["comment_id"])
    comment_found.delete()


def delete_user_report(payload):
    user_report_found = Comment.objects.get(pk=payload["user_report_id"])
    user_report_found.delete()


def archive_thread(payload):
    thread_found = Thread.objects.get(pk=payload["thread_id"])
    thread_found.archived = True
    thread_found.save()
    return thread_found
