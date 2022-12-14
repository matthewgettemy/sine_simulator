"""

"""

import time
import numpy as np
from math import sin
from math import pi
import multiprocessing


def sine(sampling_rate: int, frequency: int, amp: float, phase: float, queue: multiprocessing.Queue):
    """

    """
    interval_ms = 100
    interval_seconds = interval_ms / 1000
    samples_in_interval = int(interval_seconds * sampling_rate)
    assert(samples_in_interval >= 1)
    assert(sampling_rate < 50000)  # conservative measured loop time, can't go faster than this
    assert(sampling_rate >= (2 * frequency))  # nyquist

    produced = 0
    t_end = None
    while True:
        # t_start = t_end or time.perf_counter()
        # t_start = time.perf_counter()
        t_start = time.time()
        t_end = t_start + interval_seconds
        ts = np.linspace(t_start, t_end, samples_in_interval)
        xs = 2 * pi * frequency * ts
        ys = amp * np.sin(xs + phase)
        noise = np.random.normal(0, amp * 0.05, len(ys))
        ys += noise
        queue.put({
            "x": list(ts),
            "y": list(ys),
            "sampling_rate": sampling_rate,
            "frequency": frequency,
            "amplitude": amp,
            "phase": phase
        })

        produced += samples_in_interval
        # print(produced)

        execution_time = (time.perf_counter() - t_start)
        time_to_sleep = max((interval_seconds - execution_time), 0)
        # print(time_to_sleep)
        # time.sleep(time_to_sleep)
        time.sleep(interval_seconds)


if __name__ == "__main__":
    q = multiprocessing.Queue()
    sine_process = multiprocessing.Process(target=sine, kwargs={
        "sampling_rate": 10,
        "frequency": 1,
        "amp": 1,
        "phase": 0,
        "queue": q
    })
    sine_process.start()

    while True:
        data = q.get(block=True)
