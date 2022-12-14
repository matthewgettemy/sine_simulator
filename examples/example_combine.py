"""

"""


import multiprocessing

from broker.producer import producer
from broker.consumer import consumer
from sine import sine
from combine import combine
from fft import streaming_fft


def main():

    sine_queue = multiprocessing.Queue()
    combine_queue = multiprocessing.Queue()
    produce_combine_queue = multiprocessing.Queue()
    total_queue = multiprocessing.Queue()
    fft_input_queue = multiprocessing.Queue()
    fft_output_queue = multiprocessing.Queue()


    sine_process_1 = multiprocessing.Process(
        target=sine,
        kwargs={
            "sampling_rate": 100,
            "frequency": 1.0,
            "amp": 10.0,
            "phase": 0,
            "queue": sine_queue
        }
    )

    sine_process_2 = multiprocessing.Process(
        target=sine,
        kwargs={
            "sampling_rate": 100,
            "frequency": 3.0,
            "amp": 6.0,
            "phase": 0,
            "queue": sine_queue
        }
    )

    sine_process_3 = multiprocessing.Process(
        target=sine,
        kwargs={
            "sampling_rate": 100,
            "frequency": 8.0,
            "amp": 2.0,
            "phase": 0.0,
            "queue": sine_queue
        }
    )

    sine_producer_process = multiprocessing.Process(
        target=producer,
        kwargs={
            "topic": "sine",
            "broker_address": "localhost:9092",
            "queue": sine_queue
        }
    )

    combine_consumer_process = multiprocessing.Process(
        target=consumer,
        kwargs={
            "topics": ["sine"],
            "broker_address": "localhost:9092",
            "queue": combine_queue
        }
    )

    combine_process = multiprocessing.Process(
        target=combine,
        kwargs={
            "input_queue": combine_queue,
            "output_queue": produce_combine_queue
        }
    )

    combine_producer_process = multiprocessing.Process(
        target=producer,
        kwargs={
            "topic": "combine",
            "broker_address": "localhost:9092",
            "queue": produce_combine_queue
        }
    )

    total_consumer = multiprocessing.Process(
        target=consumer,
        kwargs={
            "topics": ["combine"],
            "broker_address": "localhost:9092",
            "queue": total_queue
        }
    )

    fft_consumer_process = multiprocessing.Process(
        target=consumer,
        kwargs={
            "topics": ["combine"],
            "broker_address": "localhost:9092",
            "queue": fft_input_queue
        }
    )

    fft_process = multiprocessing.Process(
        target=streaming_fft,
        kwargs={
            "window_size": 8192,
            "input_queue": fft_input_queue,
            "output_queue": fft_output_queue
        }
    )

    fft_producer_process = multiprocessing.Process(
        target=producer,
        kwargs={
            "topic": "fft",
            "broker_address": "localhost:9092",
            "queue": fft_output_queue
        }
    )

    sine_process_1.start()
    sine_process_2.start()
    sine_process_3.start()
    sine_producer_process.start()
    combine_consumer_process.start()
    combine_process.start()
    combine_producer_process.start()
    total_consumer.start()
    fft_consumer_process.start()
    fft_process.start()
    fft_producer_process.start()

    while True:
        data = total_queue.get()
        print(data)


if __name__ == "__main__":
    main()
