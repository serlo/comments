from .tasks import (
    create_comment,
    create_thread,
    delete_comment,
    delete_thread,
    archive_thread,
)


def execute_message(data):
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
    if data["type"] == "archive-thread":
        archive_thread(data["payload"])
        return data
    raise Exception('Invalid message')