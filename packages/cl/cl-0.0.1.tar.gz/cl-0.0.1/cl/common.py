"""cl.common"""

from __future__ import absolute_import, with_statement

import socket

from collections import deque
from itertools import count

from kombu import Consumer
from kombu import serialization
from kombu.utils import gen_unique_id as uuid   # noqa

from .pools import producers

__all__ = ["maybe_declare", "itermessages", "send_reply", "collect_replies"]
_declared_entities = set()


def maybe_declare(entity, channel):
    if entity not in _declared_entities:
        entity(channel).declare()
        _declared_entities.add(entity)


def itermessages(conn, channel, queue, limit=1, timeout=None, **kwargs):
    acc = deque()

    def on_message(body, message):
        acc.append((body, message))

    with Consumer(channel, [queue], callbacks=[on_message], **kwargs):
        for i in limit and xrange(limit) or count():
            try:
                conn.drain_events(timeout=timeout)
            except socket.timeout:
                break
            else:
                try:
                    yield acc.popleft()
                except IndexError:
                    pass


def send_reply(conn, exchange, req, msg, **props):
    with producers[conn].acquire(block=True) as producer:
        content_type = req.properties["content_type"]
        serializer = serialization.registry.type_to_name[content_type]
        maybe_declare(exchange, producer.channel)
        producer.publish(msg, exchange=exchange,
            **dict({"routing_key": req.properties["reply_to"],
                    "correlation_id": req.properties.get("correlation_id"),
                    "serializer": serializer},
                    **props))


def collect_replies(conn, channel, queue, *args, **kwargs):
    no_ack = kwargs.setdefault("no_ack", True)
    received = False
    for body, message in itermessages(conn, channel, queue, *args, **kwargs):
        if not no_ack:
            message.ack()
        received = True
        yield body
    if received:
        channel.after_reply_message_received(queue.name)
