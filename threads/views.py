from django.shortcuts import render
from django.http import JsonResponse
from threads.models import Entity


def index(request, content_provider_id, entity_id):
    try:
        entity = Entity.objects.get(
            provider_id=content_provider_id, entity_id=entity_id
        )
    except Entity.DoesNotExist:
        return JsonResponse([], safe=False)
    threads = entity.thread_set.all()
    thread_list = [thread.to_json() for thread in threads]
    return JsonResponse(thread_list, safe=False)
