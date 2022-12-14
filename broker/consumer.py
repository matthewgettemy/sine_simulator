"""

"""

import json
import multiprocessing
from queue import Empty
from kafka import KafkaConsumer


def consumer(topics: [str], broker_address: str, queue: multiprocessing.Queue):
    kafka_consumer = KafkaConsumer(
        bootstrap_servers=broker_address,
        value_deserializer=lambda v: json.loads(v)
    )
    print(f"Starting consumer on topics: {', '.join(topics)}.")
    kafka_consumer.subscribe(topics)
    for message in kafka_consumer:
        queue.put(message)


if __name__ == "__main__":
    # test the producer
    q = multiprocessing.Queue()
    consumer_process = multiprocessing.Process(
        target=consumer,
        kwargs={
            "topics": ["sine"],
            "broker_address": "localhost:9092",
            "queue": q
        }
    )
    consumer_process.start()

    while True:
        message = q.get(block=True)
        # print(message.value)
