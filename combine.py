"""

"""


import multiprocessing
import numpy as np


def add_arrays(a, b):
    if len(a) < len(b):
        c = b.copy()
        c[:len(a)] += a
    else:
        c = a.copy()
        c[:len(b)] += b
    return c


def combine(input_queue: multiprocessing.Queue, output_queue: multiprocessing.Queue):

    frequencies = []
    # x_total = np.array([])
    y_total = np.array([])
    while True:
        message = input_queue.get(block=True)
        frequency = message.value["frequency"]
        if frequency not in frequencies:
            # total += np.array(message.value["y"])
            # x_total = add_arrays(x_total, np.array(message.value["x"]))
            y_total = add_arrays(y_total, np.array(message.value["y"]))
            frequencies.append(frequency)
        else:
            data = {
                "x": list(message.value["x"]),
                "y": list(y_total),
                "sampling_rate": message.value["sampling_rate"]
            }
            output_queue.put(data)

            # reset data
            frequencies = []
            # x_total = np.array([])
            y_total = np.array([])
