from typing import Any, TypedDict

from .tasks import (
    create_thread,
    archive_thread,
    unarchive_thread,
    trash_thread,
    restore_thread,
    delete_thread,
    create_comment,
    edit_comment,
    trash_comment,
    restore_comment,
    delete_comment,
    create_user_report,
    delete_user_report,
    replace_user,
)


class Message(TypedDict):
    type: str
    payload: Any


def execute_message(data: Message) -> Message:
    if data["type"] == "create-thread":
        thread = create_thread(data["payload"])
        data["payload"]["id"] = thread.id
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
    if data["type"] == "delete-thread":
        delete_thread(data["payload"])
        return data
    if data["type"] == "create-comment":
        comment = create_comment(data["payload"])
        data["payload"]["id"] = comment.id
        return data
    if data["type"] == "edit-comment":
        edit_comment(data["payload"])
        return data
    if data["type"] == "trash-comment":
        trash_comment(data["payload"])
        return data
    if data["type"] == "restore-comment":
        restore_comment(data["payload"])
        return data
    if data["type"] == "delete-comment":
        delete_comment(data["payload"])
        return data
    if data["type"] == "create-user-report":
        user_report = create_user_report(data["payload"])
        data["payload"]["id"] = user_report.id
        return data
    if data["type"] == "delete-user-report":
        delete_user_report(data["payload"])
        return data
    if data["type"] == "replace-user":
        replace_user(data["payload"])
        return data

    raise Exception("Invalid message")
