from django.shortcuts import render
from datetime import datetime
from django.http import JsonResponse, HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from threads.models import Entity, User, Thread, Comment
from threads.tasks import create_thread
from threads.worker import execute_message as execute
import json
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


@csrf_exempt
def set_state(request: HttpRequest) -> JsonResponse:
    data = json.loads(request.body)
    consumer = data["consumer"]
    state = data["state"]
    if consumer == "serlo.org" and state == "no threads exist":
        Thread.objects.all().delete()
    if consumer == "serlo.org" and state == "one thread for entity 234 exists":
        create_thread(
            {
                "entity": {"provider_id": "serlo.org", "id": "234"},
                "user": {"provider_id": "serlo.org", "id": "456",},
                "created_at": datetime.now().isoformat(timespec="seconds"),
                "title": "Antwort auf Frage XY",
                "content": "Ich habe folgende Frage",
            }
        )
    return JsonResponse({})


@csrf_exempt
def execute_message(request: HttpRequest) -> JsonResponse:
    payload = json.loads(request.body)
    execute(payload)
    return JsonResponse({})
