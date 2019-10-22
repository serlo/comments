from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from threads.models import Entity, Author, Thread, Comment
import json


def index(request, content_provider_id, entity_id):
    if request.method == "GET":
        try:
            entity = Entity.objects.get(
                provider_id=content_provider_id, entity_id=entity_id
            )
        except Entity.DoesNotExist:
            return JsonResponse([], safe=False)
        threads = entity.thread_set.all()
        thread_list = [thread.to_json() for thread in threads]
        return JsonResponse(thread_list, safe=False)
    elif request.method == "POST":
        json_data = json.loads(request.body)

        entity, _ = Entity.objects.get_or_create(
            provider_id=content_provider_id, entity_id=entity_id
        )
        author, _ = Author.objects.get_or_create(
            user_id=json_data["author"]["user_id"],
            provider_id=json_data["author"]["provider_id"],
        )

        thread = Thread.objects.create(title=json_data["title"], entity=entity)
        comment = Comment.objects.create(
            author=author, content=json_data["content"], thread=thread
        )
        return HttpResponse()


def create_comment(request, thread_id):
    json_data = json.loads(request.body)

    author, _ = Author.objects.get_or_create(
        user_id=json_data["author"]["user_id"],
        provider_id=json_data["author"]["provider_id"],
    )
    thread = Thread.objects.get(pk=thread_id)
    comment = Comment.objects.create(
        author=author, content=json_data["content"], thread=thread
    )
    return HttpResponse()
