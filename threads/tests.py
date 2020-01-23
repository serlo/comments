from datetime import timezone, datetime
from typing import List, Any

from django.test import TestCase
from django.urls import reverse

from . import fixtures
from . import models
from . import tasks


def normalize_timestamp(timestamp: str) -> str:
    dt = datetime.fromisoformat(timestamp)
    return dt.astimezone(tz=timezone.utc).isoformat(timespec="seconds")


class ThreadIndexViewTests(TestCase):
    def test_no_threads(self) -> None:
        self.assertResponseForEntity(fixtures.entity_payloads[0], [])

    def test_one_thread(self) -> None:
        payload = fixtures.create_thread_payloads[0]
        thread = tasks.create_thread(payload)
        comments = list(thread.comment_set.all())
        self.assertResponseForEntity(
            payload["entity"],
            [
                {
                    "id": str(thread.id),
                    "title": payload["title"],
                    "comments": [
                        {
                            "id": str(comments[0].id),
                            "content": payload["content"],
                            "user": payload["user"],
                            "created_at": normalize_timestamp(payload["created_at"]),
                            "updated_at": normalize_timestamp(payload["created_at"]),
                        }
                    ],
                    "created_at": normalize_timestamp(payload["created_at"]),
                    "updated_at": normalize_timestamp(payload["created_at"]),
                }
            ],
        )

    def test_different_entity(self) -> None:
        tasks.create_thread(fixtures.create_thread_payloads[0])
        self.assertResponseForEntity(fixtures.entity_payloads[1], [])

    def test_two_comments(self) -> None:
        thread_payload = fixtures.create_thread_payloads[0]
        thread = tasks.create_thread(thread_payload)
        comment_payload: tasks.CreateCommentPayload = {
            "user": fixtures.user_payloads[1],
            "content": "Ich habe eine weitere Frage",
            "thread_id": str(thread.id),
            "created_at": "2019-11-11 11:11:11+02:00",
        }
        comment = tasks.create_comment(comment_payload)
        comments = list(thread.comment_set.all())
        self.assertResponseForEntity(
            thread_payload["entity"],
            [
                {
                    "id": str(thread.id),
                    "title": thread_payload["title"],
                    "comments": [
                        {
                            "id": str(comments[0].id),
                            "content": thread_payload["content"],
                            "user": thread_payload["user"],
                            "created_at": normalize_timestamp(
                                thread_payload["created_at"]
                            ),
                            "updated_at": normalize_timestamp(
                                thread_payload["created_at"]
                            ),
                        },
                        {
                            "id": str(comment.id),
                            "content": comment_payload["content"],
                            "user": comment_payload["user"],
                            "created_at": normalize_timestamp(
                                comment_payload["created_at"]
                            ),
                            "updated_at": normalize_timestamp(
                                comment_payload["created_at"]
                            ),
                        },
                    ],
                    "created_at": normalize_timestamp(thread_payload["created_at"]),
                    "updated_at": normalize_timestamp(comment_payload["created_at"]),
                }
            ],
        )

    def assertResponseForEntity(
        self, entity: tasks.EntityPayload, threads: Any
    ) -> None:
        url = reverse(
            "threads:index",
            kwargs={
                "content_provider_id": entity["provider_id"],
                "entity_id": entity["id"],
            },
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, threads)


class CreateThreadTaskTests(TestCase):
    def test_create_thread(self) -> None:
        payload = fixtures.create_thread_payloads[0]
        tasks.create_thread(payload)
        entity = models.Entity.objects.get(
            provider_id=payload["entity"]["provider_id"],
            entity_id=payload["entity"]["id"],
        )
        threads = list(entity.thread_set.all())
        self.assertEqual(len(threads), 1)
        self.assertEqual(threads[0].title, payload["title"])
        self.assertEqual(
            list(threads[0].comment_set.all())[0].content, payload["content"]
        )

    def test_create_entity_and_user_only_once(self) -> None:
        payload = fixtures.create_thread_payloads[0]
        tasks.create_thread(payload)
        tasks.create_thread(payload)
        models.User.objects.get(**payload["user"])
        models.Entity.objects.get(
            provider_id=payload["entity"]["provider_id"],
            entity_id=payload["entity"]["id"],
        )


class CreateCommentTaskTests(TestCase):
    def test_create_comment(self) -> None:
        thread_payload = fixtures.create_thread_payloads[0]
        thread = tasks.create_thread(thread_payload)
        comment_payload: tasks.CreateCommentPayload = {
            "user": fixtures.user_payloads[1],
            "content": "Ich habe eine weitere Frage",
            "thread_id": str(thread.id),
            "created_at": "2019-11-11 11:11:11+02:00",
        }
        tasks.create_comment(comment_payload)
        thread = models.Thread.objects.get(pk=thread.id)
        comments = list(thread.comment_set.all())
        self.assertEqual(len(comments), 2)
        self.assertEqual(comments[1].content, comment_payload["content"])


class CreateUserReportView(TestCase):
    def test_create_user_report_with_thread(self) -> None:
        thread_payload = fixtures.create_thread_payloads[0]
        thread = tasks.create_thread(thread_payload)
        user_report_payload: tasks.CreateUserReportPayload = {
            "thread_id": str(thread.id),
            "comment_id": None,
            "user": fixtures.user_payloads[0],
            "created_at": "2019-12-12 12:12:12+02:00",
            "description": "Thread Titel ist beleidigend",
            "category": "OFFENSIVE",
        }
        tasks.create_user_report(user_report_payload)
        user_report_found = models.UserReport.objects.get(
            description="Thread Titel ist beleidigend"
        )
        self.assertEqual(
            user_report_found.description, user_report_payload["description"]
        )
        self.assertEqual(user_report_found.category, user_report_payload["category"])
        self.assertEqual(user_report_found.thread, thread)
        self.assertEqual(user_report_found.comment, None)

    def test_create_user_report_with_thread_and_comment(self) -> None:
        thread_payload = fixtures.create_thread_payloads[0]
        thread = tasks.create_thread(thread_payload)
        comment_payload: tasks.CreateCommentPayload = {
            "user": fixtures.user_payloads[1],
            "content": "Ich habe eine weitere Frage",
            "thread_id": str(thread.id),
            "created_at": "2019-11-11 11:11:11+02:00",
        }
        comment = tasks.create_comment(comment_payload)
        user_report_payload: tasks.CreateUserReportPayload = {
            "thread_id": str(thread.id),
            "comment_id": str(comment.id),
            "user": fixtures.user_payloads[0],
            "created_at": "2019-12-12 12:12:12+02:00",
            "description": "Thread Titel ist beleidigend",
            "category": "OFFENSIVE",
        }
        tasks.create_user_report(user_report_payload)
        user_report_found = models.UserReport.objects.get(
            description="Thread Titel ist beleidigend"
        )
        self.assertEqual(
            user_report_found.description, user_report_payload["description"]
        )
        self.assertEqual(user_report_found.category, user_report_payload["category"])
        self.assertEqual(user_report_found.thread, thread)
        self.assertEqual(user_report_found.comment, comment)


class DeleteThreadTaskTests(TestCase):
    def test_delete_existing_thread(self) -> None:
        thread = tasks.create_thread(fixtures.create_thread_payloads[0])
        tasks.delete_thread({"thread_id": str(thread.id)})
        self.assertEqual(models.Thread.objects.count(), 0)

    def test_delete_nonexisting_thread(self) -> None:
        self.assertRaises(
            models.Thread.DoesNotExist,
            tasks.delete_thread,
            {"thread_id": "c64ff5cb-2a21-47e5-89f7-55fad67c0eb9"},
        )


class DeleteCommentTaskTests(TestCase):
    def test_delete_existing_comment(self) -> None:
        thread_payload = fixtures.create_thread_payloads[0]
        thread = tasks.create_thread(thread_payload)
        comment_payload: tasks.CreateCommentPayload = {
            "user": fixtures.user_payloads[1],
            "content": "Ich habe eine weitere Frage",
            "thread_id": str(thread.id),
            "created_at": "2019-11-11 11:11:11+02:00",
        }
        comment = tasks.create_comment(comment_payload)
        tasks.delete_comment({"comment_id": str(comment.id)})
        self.assertEqual(models.Comment.objects.count(), 1)

    def test_delete_nonexisting_comment(self) -> None:
        self.assertRaises(
            models.Comment.DoesNotExist,
            tasks.delete_comment,
            {"comment_id": "c64ff5cb-2a21-47e5-89f7-55fad67c0eb9"},
        )


class ArchiveThreadView(TestCase):
    def test_archive_thread(self) -> None:
        thread = tasks.create_thread(fixtures.create_thread_payloads[0])
        thread = tasks.archive_thread({"thread_id": str(thread.id)})
        thread = models.Thread.objects.get(pk=thread.id)
        self.assertEqual(thread.archived, True)

    def test_archive_nonexisting_thread(self) -> None:
        self.assertRaises(
            models.Thread.DoesNotExist,
            tasks.archive_thread,
            {"thread_id": "c64ff5cb-2a21-47e5-89f7-55fad67c0eb9"},
        )


class UnarchiveThreadView(TestCase):
    def test_unarchive_thread(self) -> None:
        thread = tasks.create_thread(fixtures.create_thread_payloads[0])
        thread = tasks.archive_thread({"thread_id": str(thread.id)})
        thread = tasks.unarchive_thread({"thread_id": str(thread.id)})
        thread = models.Thread.objects.get(pk=thread.id)
        self.assertEqual(thread.archived, False)

    def test_unarchive_nonexisting_thread(self) -> None:
        self.assertRaises(
            models.Thread.DoesNotExist,
            tasks.unarchive_thread,
            {"thread_id": "c64ff5cb-2a21-47e5-89f7-55fad67c0eb9"},
        )


class EditCommentTaskTests(TestCase):
    def test_edit_comment(self) -> None:
        thread_payload = fixtures.create_thread_payloads[0]
        thread = tasks.create_thread(thread_payload)
        comment_payload: tasks.CreateCommentPayload = {
            "user": fixtures.user_payloads[1],
            "content": "Ich habe eine weitere Frage",
            "thread_id": str(thread.id),
            "created_at": "2019-11-11 11:11:11+02:00",
        }
        comment = tasks.create_comment(comment_payload)
        edit_comment_payload: tasks.EditCommentPayload = {
            "comment_id": str(comment.id),
            "content": "Ich habe doch keine Frage",
            "created_at": "2019-11-11 11:11:12+02:00",
        }
        tasks.edit_comment(edit_comment_payload)
        thread = models.Thread.objects.get(pk=thread.id)
        comment = models.Comment.objects.get(pk=comment.id)
        self.assertEqual(comment.content, edit_comment_payload["content"])
        self.assertEqual(
            comment.updated_at,
            tasks.datetime_from_timestamp(edit_comment_payload["created_at"]),
        )
        self.assertEqual(
            thread.updated_at,
            tasks.datetime_from_timestamp(edit_comment_payload["created_at"]),
        )

    def test_edit_nonexisting_comment(self) -> None:
        self.assertRaises(
            models.Comment.DoesNotExist,
            tasks.edit_comment,
            {
                "comment_id": "c64ff5cb-2a21-47e5-89f7-55fad67c0eb9",
                "content": "Ich habe doch keine Frage",
                "created_at": "2019-11-11 11:11:12+02:00",
            },
        )


class TrashThreadTaskTests(TestCase):
    def test_trash_thread(self) -> None:
        thread = tasks.create_thread(fixtures.create_thread_payloads[0])
        thread = tasks.trash_thread({"thread_id": str(thread.id)})
        thread = models.Thread.objects.get(pk=thread.id)
        self.assertEqual(thread.trashed, True)

    def test_unarchive_nonexisting_thread(self) -> None:
        self.assertRaises(
            models.Thread.DoesNotExist,
            tasks.trash_thread,
            {"thread_id": "c64ff5cb-2a21-47e5-89f7-55fad67c0eb9"},
        )


class RestoreThreadTaskTests(TestCase):
    def test_restore_thread(self) -> None:
        thread = tasks.create_thread(fixtures.create_thread_payloads[0])
        thread = tasks.trash_thread({"thread_id": str(thread.id)})
        thread = tasks.restore_thread({"thread_id": str(thread.id)})
        thread = models.Thread.objects.get(pk=thread.id)
        self.assertEqual(thread.trashed, False)

    def test_restore_nonexisting_thread(self) -> None:
        self.assertRaises(
            models.Thread.DoesNotExist,
            tasks.restore_thread,
            {"thread_id": "c64ff5cb-2a21-47e5-89f7-55fad67c0eb9"},
        )


class TrashCommentTaskTests(TestCase):
    def test_trash_comment(self) -> None:
        thread = tasks.create_thread(fixtures.create_thread_payloads[0])
        comment = list(thread.comment_set.all())[0]
        comment = tasks.trash_comment({"comment_id": str(comment.id)})
        comment = models.Comment.objects.get(pk=comment.id)
        self.assertEqual(comment.trashed, True)

    def test_trash_nonexisting_comment(self) -> None:
        self.assertRaises(
            models.Comment.DoesNotExist,
            tasks.trash_comment,
            {"comment_id": "c64ff5cb-2a21-47e5-89f7-55fad67c0eb9"},
        )


class RestoreCommentTaskTests(TestCase):
    def test_restore_comment(self) -> None:
        thread = tasks.create_thread(fixtures.create_thread_payloads[0])
        comment = list(thread.comment_set.all())[0]
        comment = tasks.trash_comment({"comment_id": str(comment.id)})
        comment = tasks.restore_comment({"comment_id": str(comment.id)})
        comment = models.Comment.objects.get(pk=comment.id)
        self.assertEqual(comment.trashed, False)

    def test_restore_nonexisting_comment(self) -> None:
        self.assertRaises(
            models.Comment.DoesNotExist,
            tasks.restore_comment,
            {"comment_id": "c64ff5cb-2a21-47e5-89f7-55fad67c0eb9"},
        )


class ReplaceUserTaskTest(TestCase):
    def test_replace_user(self) -> None:
        tasks.create_thread(fixtures.create_thread_payloads[0])
        user = tasks.replace_user(
            {"old": fixtures.user_payloads[0], "new": fixtures.user_payloads[1],}
        )
        user = models.User.objects.get(pk=user.id)
        self.assertEqual(user.provider_id, fixtures.user_payloads[1]["provider_id"])
        self.assertEqual(user.user_id, fixtures.user_payloads[1]["user_id"])
        self.assertEqual(user.comment_set.count(), 1)

    def test_replace_nonexisting_user(self) -> None:
        self.assertRaises(
            models.User.DoesNotExist,
            tasks.replace_user,
            {"old": fixtures.user_payloads[0], "new": fixtures.user_payloads[1],},
        )
