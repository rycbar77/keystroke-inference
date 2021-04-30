import math
import warnings

import numpy as np
import soundfile as wav

warnings.filterwarnings("ignore")


def load(path):
    data, meta = wav.read(path)
    data = np.array(data)
    return normalize(data[:, 0].astype(float) + data[:, 1].astype(float))


def rms(series):
    return math.sqrt(sum(series ** 2) / series.size)


def normalize(series):
    return series / rms(series)


def wav_file(in_file):
    mono = load(in_file)
    return list(mono)

# see keylogger.py
