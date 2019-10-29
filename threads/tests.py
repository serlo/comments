from django.test import TestCase
from .models import Author, Entity, Thread, Comment
from . import tasks
from django.urls import reverse
import json


def create_thread(**kwargs):
    author, _ = Author.objects.get_or_create(
        user_id=kwargs["user_id"], provider_id=kwargs["user_provider_id"]
    )
    entity, _ = Entity.objects.get_or_create(
        entity_id=kwargs["entity_id"], provider_id=kwargs["content_provider_id"]
    )
    thread = Thread.objects.create(title=kwargs["title"], entity=entity)
    comment = Comment.objects.create(
        author=author, content=kwargs["content"], thread=thread
    )
    return thread


def add_comment(**kwargs):
    author = Author.objects.create(
        user_id=kwargs["user_id"], provider_id=kwargs["user_provider_id"]
    )
    comment = Comment.objects.create(
        author=author, content=kwargs["content"], thread=kwargs["thread"]
    )
    return comment


class ThreadIndexViewTests(TestCase):
    def test_no_thread(self):
        url = reverse(
            "threads:index", args=({"content_provider_id": "serlo", "entity_id": "123"})
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, [])

    def test_thread(self):
        test_thread = create_thread(
            title="Antwort auf Frage XY",
            entity_id="123",
            content_provider_id="serlo",
            user_provider_id="serlo",
            user_id="456",
            content="Ich habe folgende Frage",
        )

        test_thread_comments = list(test_thread.comment_set.all())

        url = reverse(
            "threads:index", kwargs={"content_provider_id": "serlo", "entity_id": "123"}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            [
                {
                    "id": test_thread.id,
                    "title": "Antwort auf Frage XY",
                    "comments": [
                        {
                            "id": test_thread_comments[0].id,
                            "content": "Ich habe folgende Frage",
                            "author": {"user_id": "456", "provider_id": "serlo"},
                            "created_at": test_thread_comments[
                                0
                            ].created_at.isoformat(),
                        }
                    ],
                }
            ],
        )

    def test_different_entity(self):
        test_thread = create_thread(
            title="Antwort auf Frage XY",
            entity_id="789",
            content_provider_id="serlo",
            user_provider_id="serlo",
            user_id="456",
            content="Ich habe folgende Frage",
        )
        url = reverse(
            "threads:index", kwargs={"content_provider_id": "serlo", "entity_id": "234"}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, [])

    def test_add_comment(self):
        self.maxDiff = 1000
        test_thread = create_thread(
            title="Antwort auf Frage XY",
            entity_id="123",
            content_provider_id="serlo",
            user_provider_id="serlo",
            user_id="456",
            content="Ich habe folgende Frage",
        )

        comment = add_comment(
            user_provider_id="serlo",
            user_id="101",
            content="Ich habe weitere Frage",
            thread=test_thread,
        )
        url = reverse(
            "threads:index", kwargs={"content_provider_id": "serlo", "entity_id": "123"}
        )

        test_thread_comments = list(test_thread.comment_set.all())
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            [
                {
                    "id": test_thread.id,
                    "title": "Antwort auf Frage XY",
                    "comments": [
                        {
                            "id": test_thread_comments[0].id,
                            "content": "Ich habe folgende Frage",
                            "author": {"user_id": "456", "provider_id": "serlo"},
                            "created_at": test_thread_comments[
                                0
                            ].created_at.isoformat(),
                        },
                        {
                            "id": comment.id,
                            "content": "Ich habe weitere Frage",
                            "author": {"user_id": "101", "provider_id": "serlo"},
                            "created_at": comment.created_at.isoformat(),
                        },
                    ],
                }
            ],
        )


class CreateThreadView(TestCase):
    def test_create_thread(self):
        thread = tasks.create_thread(
            {
                "author": {"provider_id": "serlo", "user_id": "456"},
                "entity": {"provider_id": "serlo", "id": "123"},
                "title": "Antwort auf Frage XY",
                "content": "Ich habe folgende Frage",
            }
        )
        entity = Entity.objects.get(
            provider_id="serlo", entity_id="123"
        )
        threads = list(entity.thread_set.all())
        self.assertEqual(len(threads), 1)
        self.assertEqual(threads[0].title, "Antwort auf Frage XY")
        self.assertEqual(
            list(threads[0].comment_set.all())[
                0].content, "Ich habe folgende Frage"
        )

    def test_create_entity_once(self):
        tasks.create_thread(
            {
                "author": {"provider_id": "serlo", "user_id": "456"},
                "entity": {"provider_id": "serlo", "id": "123"},
                "title": "Antwort auf Frage XY",
                "content": "Ich habe folgende Frage",
            }
        )
        tasks.create_thread(
            {
                "author": {"provider_id": "serlo", "user_id": "456"},
                "entity": {"provider_id": "serlo", "id": "123"},
                "title": "Antwort auf Frage XY",
                "content": "Ich habe folgende Frage",
            }
        )

        Entity.objects.get(provider_id="serlo", entity_id="123")
        Author.objects.get(provider_id="serlo", user_id="456")


class CreateCommentView(TestCase):
    def test_create_comment(self):
        thread = create_thread(
            title="Antwort auf Frage XY",
            entity_id="123",
            content_provider_id="serlo",
            user_provider_id="serlo",
            user_id="456",
            content="Ich habe folgende Frage",
        )
        tasks.create_comment(
            {
                "thread_id": thread.id,
                "author": {"provider_id": "serlo", "user_id": "456"},
                "content": "Ich habe folgende Frage",
            }
        )

        # self.assertEqual(response.status_code, 200)

        thread_found = Thread.objects.get(pk=thread.id)
        comments = list(thread_found.comment_set.all())
        self.assertEqual(len(comments), 2)
        self.assertEqual(comments[0].content, "Ich habe folgende Frage")
