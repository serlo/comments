#!/usr/bin/env python
from confluent_kafka import Consumer, KafkaException
import django
import os
import json
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()


def main():
    from threads.models import Entity
    from threads.tasks import create_comment, create_thread
    consumer = Consumer({
        'bootstrap.servers': 'kafka:29092',
        'group.id': 'commenting-systemzz',
        'auto.offset.reset': 'earliest'
    })

    consumer.subscribe(['comments', 'threads'])
    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                raise KafkaException(msg.error())
            else:
                try:
                    payload = json.loads(msg.value())

                    if msg.topic() == 'comments':
                        create_comment(payload)
                    if msg.topic() == 'threads':
                        create_thread(payload)
                except Exception as e:
                    print(msg.value())
                    print('Failed to handle message ' + str(e))

    except KeyboardInterrupt:
        sys.stderr.write('%% Aborted by user\n')

    finally:
        # Close down consumer to commit final offsets.
        consumer.close()


if __name__ == '__main__':
    main()
