"""

"""

import json
import multiprocessing
import numpy as np
from queue import Empty
from kafka import KafkaProducer


def producer(topic: str, broker_address: str, queue: multiprocessing.Queue):
    kafka_producer = KafkaProducer(
        bootstrap_servers=broker_address,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    print(f"Starting producer on topic: {topic}.")
    while True:
        try:
            data = queue.get(block=True, timeout=2)
        except Empty:
            return

        kafka_producer.send(
            topic=topic,
            # key=b"test_key",
            value=data
        )


if __name__ == "__main__":
    # test the producer
    q = multiprocessing.Queue()
    producer_process = multiprocessing.Process(
        target=producer,
        kwargs={
            "topic": "sine",
            "broker_address": "localhost:9092",
            "queue": q
        }
    )
    producer_process.start()
    for i in range(50):
        q.put(i)
