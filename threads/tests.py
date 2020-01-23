from django.test import TestCase
from .models import User, Entity, Thread, Comment, UserReport
from . import tasks
from django.urls import reverse
import json
from datetime import datetime, timezone


def create_thread(**kwargs):
    user, _ = User.objects.get_or_create(
        user_id=kwargs["user_id"], provider_id=kwargs["user_provider_id"]
    )
    entity, _ = Entity.objects.get_or_create(
        entity_id=kwargs["entity_id"], provider_id=kwargs["content_provider_id"]
    )
    thread = Thread.objects.create(title=kwargs["title"], entity=entity)
    comment = Comment.objects.create(
        user=user,
        content=kwargs["content"],
        thread=thread,
        created_at=datetime.fromisoformat(kwargs["created_at"]),
    )
    return thread


def add_comment(**kwargs):
    user = User.objects.create(
        user_id=kwargs["user_id"], provider_id=kwargs["user_provider_id"]
    )
    comment = Comment.objects.create(
        user=user,
        content=kwargs["content"],
        thread=kwargs["thread"],
        created_at=datetime.fromisoformat(kwargs["created_at"]),
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
            created_at="2019-11-11 11:11:11+02:00",
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
                    "id": str(test_thread.id),
                    "title": "Antwort auf Frage XY",
                    "comments": [
                        {
                            "id": str(test_thread_comments[0].id),
                            "content": "Ich habe folgende Frage",
                            "user": {"user_id": "456", "provider_id": "serlo"},
                            "created_at": test_thread_comments[0]
                            .created_at.astimezone(tz=timezone.utc)
                            .isoformat(),
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
            created_at="2019-11-11 11:11:11+02:00",
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
            created_at="2019-11-11 11:11:11+02:00",
        )

        comment = add_comment(
            user_provider_id="serlo",
            user_id="101",
            content="Ich habe weitere Fragen",
            thread=test_thread,
            created_at="2019-11-11 11:11:11+02:00",
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
                    "id": str(test_thread.id),
                    "title": "Antwort auf Frage XY",
                    "comments": [
                        {
                            "id": str(test_thread_comments[0].id),
                            "content": "Ich habe folgende Frage",
                            "user": {"user_id": "456", "provider_id": "serlo"},
                            "created_at": test_thread_comments[0]
                            .created_at.astimezone(tz=timezone.utc)
                            .isoformat(),
                        },
                        {
                            "id": str(comment.id),
                            "content": "Ich habe weitere Fragen",
                            "user": {"user_id": "101", "provider_id": "serlo"},
                            "created_at": comment.created_at.astimezone(
                                tz=timezone.utc
                            ).isoformat(),
                        },
                    ],
                }
            ],
        )


class CreateThreadView(TestCase):
    def test_create_thread(self):
        thread = tasks.create_thread(
            {
                "user": {"provider_id": "serlo", "user_id": "456"},
                "entity": {"provider_id": "serlo", "id": "123"},
                "title": "Antwort auf Frage XY",
                "content": "Ich habe folgende Frage",
                "created_at": "2019-11-11 11:11:11+02:00",
            }
        )
        entity = Entity.objects.get(provider_id="serlo", entity_id="123")
        threads = list(entity.thread_set.all())
        self.assertEqual(len(threads), 1)
        self.assertEqual(threads[0].title, "Antwort auf Frage XY")
        self.assertEqual(
            list(threads[0].comment_set.all())[0].content, "Ich habe folgende Frage"
        )

    def test_create_entity_once(self):
        tasks.create_thread(
            {
                "user": {"provider_id": "serlo", "user_id": "456"},
                "entity": {"provider_id": "serlo", "id": "123"},
                "title": "Antwort auf Frage XY",
                "content": "Ich habe folgende Frage",
                "created_at": "2019-11-11 11:11:11+02:00",
            }
        )
        tasks.create_thread(
            {
                "user": {"provider_id": "serlo", "user_id": "456"},
                "entity": {"provider_id": "serlo", "id": "123"},
                "title": "Antwort auf Frage XY",
                "content": "Ich habe folgende Frage",
                "created_at": "2019-11-11 11:11:11+02:00",
            }
        )

        Entity.objects.get(provider_id="serlo", entity_id="123")
        User.objects.get(provider_id="serlo", user_id="456")


class CreateCommentView(TestCase):
    def test_create_comment(self):
        thread = create_thread(
            title="Antwort auf Frage XY",
            entity_id="123",
            content_provider_id="serlo",
            user_provider_id="serlo",
            user_id="456",
            content="Ich habe folgende Frage",
            created_at="2019-11-11 11:11:11+02:00",
        )
        tasks.create_comment(
            {
                "thread_id": thread.id,
                "user": {"provider_id": "serlo", "user_id": "456"},
                "content": "Ich habe folgende Frage",
                "created_at": "2019-11-11 11:11:11+02:00",
            }
        )

        # self.assertEqual(response.status_code, 200)

        thread_found = Thread.objects.get(pk=thread.id)
        comments = list(thread_found.comment_set.all())
        self.assertEqual(len(comments), 2)
        self.assertEqual(comments[0].content, "Ich habe folgende Frage")


class CreateUserReportView(TestCase):
    def test_create_user_report_with_thread(self):
        thread = create_thread(
            title="Antwort auf Frage XY",
            entity_id="123",
            content_provider_id="serlo",
            user_provider_id="serlo",
            user_id="456",
            content="Ich habe folgende Frage",
            created_at="2019-11-11 11:11:11+02:00",
        )
        tasks.create_user_report(
            {
                "thread_id": thread.id,
                "comment_id": None,
                "user": {"provider_id": "serlo", "user_id": "456"},
                "created_at": "2019-12-12 12:12:12+02:00",
                "description": "Thread Titel ist beleidigend",
                "category": "OFFENSIVE",
            }
        )

        user_report_found = UserReport.objects.get(
            description="Thread Titel ist beleidigend"
        )

        self.assertEqual(user_report_found.description, "Thread Titel ist beleidigend")
        self.assertEqual(user_report_found.category, "OFFENSIVE")
        self.assertEqual(user_report_found.thread, thread)
        self.assertEqual(user_report_found.comment, None)

    def test_create_user_report_with_thread_and_comment(self):
        thread = create_thread(
            title="Antwort auf Frage XY",
            entity_id="123",
            content_provider_id="serlo",
            user_provider_id="serlo",
            user_id="456",
            content="Ich habe folgende Frage",
            created_at="2019-11-11 11:11:11+02:00",
        )

        comment = add_comment(
            user_provider_id="serlo",
            user_id="101",
            content="Ich habe weitere Fragen",
            thread=thread,
            created_at="2019-11-11 11:11:11+02:00",
        )

        tasks.create_user_report(
            {
                "thread_id": thread.id,
                "comment_id": comment.id,
                "user": {"provider_id": "serlo", "user_id": "456"},
                "created_at": "2019-12-12 12:12:12+02:00",
                "description": "Thread Titel ist beleidigend",
                "category": "OFFENSIVE",
            }
        )

        user_report_found = UserReport.objects.get(
            description="Thread Titel ist beleidigend"
        )

        self.assertEqual(user_report_found.description, "Thread Titel ist beleidigend")
        self.assertEqual(user_report_found.category, "OFFENSIVE")
        self.assertEqual(user_report_found.thread, thread)
        self.assertEqual(user_report_found.comment, comment)


class DeleteThreadView(TestCase):
    def test_delete_existing_thread(self):
        thread = create_thread(
            title="Antwort auf Frage XY",
            entity_id="123",
            content_provider_id="serlo",
            user_provider_id="serlo",
            user_id="456",
            content="Ich habe folgende Frage",
            created_at="2019-11-11 11:11:11+02:00",
        )

        tasks.delete_thread({"thread_id": thread.id})

        self.assertEqual(Thread.objects.count(), 0)

    def test_delete_nonexisting_thread(self):
        self.assertRaises(
            Thread.DoesNotExist,
            tasks.delete_thread,
            {"thread_id": "c64ff5cb-2a21-47e5-89f7-55fad67c0eb9"},
        )


class DeleteCommentView(TestCase):
    def test_delete_existing_comment(self):
        thread = create_thread(
            title="Antwort auf Frage XY",
            entity_id="123",
            content_provider_id="serlo",
            user_provider_id="serlo",
            user_id="456",
            content="Ich habe folgende Frage",
            created_at="2019-11-11 11:11:11+02:00",
        )

        comment = add_comment(
            user_provider_id="serlo",
            user_id="101",
            content="Ich habe weitere Fragen",
            thread=thread,
            created_at="2019-11-11 11:11:11+02:00",
        )

        tasks.delete_comment({"comment_id": comment.id})

        self.assertEqual(Comment.objects.count(), 1)

    def test_delete_nonexisting_comment(self):
        self.assertRaises(
            Comment.DoesNotExist,
            tasks.delete_comment,
            {"comment_id": "c64ff5cb-2a21-47e5-89f7-55fad67c0eb9"},
        )


class ArchiveThreadView(TestCase):
    def test_archive_thread(self):
        thread = create_thread(
            title="Antwort auf Frage XY",
            entity_id="123",
            content_provider_id="serlo",
            user_provider_id="serlo",
            user_id="456",
            content="Ich habe folgende Frage",
            created_at="2019-11-11 11:11:11+02:00",
        )
        thread = tasks.archive_thread({"thread_id": thread.id})

        self.assertEqual(thread.archived, True)
