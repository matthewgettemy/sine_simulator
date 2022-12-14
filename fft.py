"""

"""

from math import sqrt
import numpy as np
import multiprocessing
from collections import deque
from scipy.fftpack import fft, fftfreq


def streaming_fft(window_size: int, input_queue: multiprocessing.Queue, output_queue: multiprocessing.Queue):
    window = deque([0 for _ in range(window_size)], maxlen=window_size)
    hann = np.hanning(window_size)
    while True:
        message = input_queue.get()
        sampling_rate = message.value["sampling_rate"]
        window.extend(message.value["y"])
        # y = fft(window * hann)
        y = fft(window)

        # normalize
        y *= (2/len(window))

        N = len(y)
        n = np.arange(N)
        T = N / sampling_rate
        frequencies = n / T

        data = {
            "x": list(frequencies)[:N//2],
            "y": list(np.abs(y))[:N//2],
            "sampling_rate": sampling_rate
        }

        output_queue.put(data)



"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft, ifft
# sampling rate
sr = 2000
# sampling interval
ts = 1.0/sr
t = np.arange(0,1,ts)

freq = 1.
x = 3*np.sin(2*np.pi*freq*t)

freq = 4
x += np.sin(2*np.pi*freq*t)

freq = 7
x += 0.5* np.sin(2*np.pi*freq*t)

plt.figure(figsize = (8, 6))
plt.plot(t, x, 'r')
plt.ylabel('Amplitude')

plt.show()

X = fft(x)
N = len(X)
n = np.arange(N)
T = N/sr
freq = n/T

plt.figure(figsize = (12, 6))
plt.subplot(121)

plt.stem(freq, np.abs(X), 'b', markerfmt=" ", basefmt="-b")
plt.xlabel('Freq (Hz)')
plt.ylabel('FFT Amplitude |X(freq)|')
plt.xlim(0, 10)

plt.subplot(122)
plt.plot(t, ifft(X), 'r')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.tight_layout()
plt.show()
"""