from django.shortcuts import render
from datetime import datetime
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from threads.models import Entity, Author, Thread, Comment
from threads.tasks import create_thread
import json
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

@csrf_exempt
def index(request):
    logger.error('Hey')
    if request.method == 'GET':
        return JsonResponse({
            "serlo.org": [
                "no threads exist",
                "one thread for entity 234 exist"
            ]
        })
    elif request.method == 'POST':
        data = json.loads(request.body)
        consumer = data['consumer']
        state = data['state']
        if consumer == 'serlo.org' and state == 'no threads exist':
            Thread.objects.all().delete()
        if consumer == 'serlo.org' and state == 'one thread for entity 234 exist':
            create_thread({
                "entity": {
                    "provider_id": "serlo.org",
                    "id": "234"
                },
                "author": {
                    "provider_id": "serlo.org",
                    "user_id": "456",
                },
                "created_at": datetime.now().isoformat(timespec='seconds'),
                "title": "Antwort auf Frage XY",
                "content": "Ich habe folgende Frage"
            })
        return JsonResponse({})



