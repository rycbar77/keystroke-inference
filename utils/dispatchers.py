import math
import warnings

import numpy as np
from matplotlib import pyplot as plt
from config import dispatcher_threshold
warnings.filterwarnings("ignore")


def rms(series):
    return math.sqrt(sum(series ** 2) / series.size)


def normalize(series):
    return series / rms(series)


def dispatcher(data, interact=False):
    out = []
    rem = len(data) % 441
    data = np.array(data[:len(data) - rem])
    minimum_interval = 8000
    sample_length = (44100 * 100) // 1000

    peaks = []
    for x in range(0, len(data) - 440):
        peaks.append(np.sum(np.absolute(np.fft.fft(data[x:x + 440]))))
    peaks = np.array(peaks)
    threshold = dispatcher_threshold
    tau = np.percentile(peaks, threshold)
    if interact:
        while threshold != -1:
            tau = np.percentile(peaks, threshold)
            plt.plot(peaks)
            plt.axhline(y=tau, ls="-", c="red")
            plt.show()
            threshold = float(input("Choose a threshold in [0,100], input nothing or -1 to confirm.\n") or -1)
            if threshold > 100 or (threshold < 0 and threshold != -1):
                raise Exception("Invalid threshold")
    x = 0
    step = 1
    past_x = - minimum_interval - step
    idx = 0
    while x < peaks.size:
        if peaks[x] >= tau:
            if x - past_x >= minimum_interval:
                keypress = normalize(data[x:x + sample_length])
                past_x = x
                out.append([idx, keypress])
                idx += 1
            x = past_x + minimum_interval
        else:
            x += step

    return out
