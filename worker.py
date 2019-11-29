#!/usr/bin/env python
from confluent_kafka import Consumer, KafkaException, Producer
import django
import os
import json
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()


def main():
    from threads.models import Entity
    from threads.tasks import (
        create_comment,
        create_thread,
        delete_comment,
        delete_thread,
        archive_thread,


    consumer = Consumer(
        {
            "bootstrap.servers": "kafka:29092",
            "group.id": "commenting-system",
            "auto.offset.reset": "earliest",
        }
    )

    producer = Producer({"bootstrap.servers": "kafka:29092"})

    def delivery_report(err, msg):
        if err:
            sys.stderr.write("%% Message failed delivery: %s\n" % err)
        else:
            sys.stderr.write(
                "%% Message delivered to %s [%d] @ %d\n"
                % (msg.topic(), msg.partition(), msg.offset())
            )

    consumer.subscribe(["comments-queue"])
    try:
        while True:
            producer.poll(0)
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                raise KafkaException(msg.error())
            else:
                try:
                    data = json.loads(msg.value())

                    if data["type"] == "create-comment":
                        comment = create_comment(data["payload"])
                        data["payload"]["id"] = comment.id

                    if data["type"] == "create-thread":
                        thread = create_thread(data["payload"])
                        data["payload"]["id"] = thread.id

                    if data["type"] == "delete-thread":
                        delete_thread(data["payload"])

                    if data["type"] == "delete-comment":
                        delete_comment(data["payload"])

                    if data["type"] == "archive-thread":
                        thread = archive_thread(data["payload"])
                    producer.produce(
                        "comments", json.dumps(data), callback=delivery_report
                    )

                except Exception as e:
                    print(msg.value())
                    print("Failed to handle message " + str(e))

    except KeyboardInterrupt:
        sys.stderr.write("%% Aborted by user\n")

    finally:
        # Close down consumer to commit final offsets.
        consumer.close()
        producer.flush()


if __name__ == "__main__":
    main()
