from typing import List

from threads.tasks import AuthorPayload, CreateThreadPayload, EntityPayload

author_payloads: List[AuthorPayload] = [
    {"provider_id": "serlo-user", "user_id": "1-user"},
    {"provider_id": "serlo-user", "user_id": "2-user"},
]

entity_payloads: List[EntityPayload] = [
    {"provider_id": "serlo-entity", "id": "1-entity"},
    {"provider_id": "serlo-entity", "id": "2-entity"},
]

create_thread_payloads: List[CreateThreadPayload] = [
    {
        "author": author_payloads[0],
        "entity": entity_payloads[0],
        "title": "Antwort auf Frage XY",
        "content": "Ich habe folgende Frage",
        "created_at": "2019-11-11 11:11:11+02:00",
    }
]
