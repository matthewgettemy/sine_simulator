"""

"""


import multiprocessing

from broker.producer import producer
from sine import sine


def main():
    q = multiprocessing.Queue()

    sine_process = multiprocessing.Process(
        target=sine,
        kwargs={
            "sampling_rate": 10,
            "frequency": 1,
            "amp": 2,
            "phase": 0,
            "queue": q
        }
    )

    producer_process = multiprocessing.Process(
        target=producer,
        kwargs={
            "topic": "sine",
            "broker_address": "localhost:9092",
            "queue": q
        }
    )

    sine_process.start()
    producer_process.start()


if __name__ == "__main__":
    main()
