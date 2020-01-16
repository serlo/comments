from typing import Any, TypedDict

from .tasks import (
    create_comment,
    create_thread,
    delete_comment,
    delete_thread,
    archive_thread,
    edit_comment,
    unarchive_thread,
    trash_comment,
    trash_thread,
    restore_comment,
    restore_thread,
    replace_user,
)


class Message(TypedDict):
    type: str
    payload: Any


def execute_message(data: Message) -> Message:
    if data["type"] == "create-comment":
        comment = create_comment(data["payload"])
        data["payload"]["id"] = comment.id
        return data
    if data["type"] == "create-thread":
        thread = create_thread(data["payload"])
        data["payload"]["id"] = thread.id
        return data
    if data["type"] == "delete-thread":
        delete_thread(data["payload"])
        return data
    if data["type"] == "delete-comment":
        delete_comment(data["payload"])
        return data
    if data["type"] == "edit-comment":
        edit_comment(data["payload"])
        return data
    if data["type"] == "archive-thread":
        archive_thread(data["payload"])
        return data
    if data["type"] == "unarchive-thread":
        unarchive_thread(data["payload"])
        return data
    if data["type"] == "trash-thread":
        trash_thread(data["payload"])
        return data
    if data["type"] == "restore-thread":
        restore_thread(data["payload"])
        return data
    if data["type"] == "trash-comment":
        trash_comment(data["payload"])
        return data
    if data["type"] == "restore-comment":
        restore_comment(data["payload"])
        return data
    if data["type"] == "replace-user":
        replace_user(data["payload"])
        return data

    raise Exception("Invalid message")
