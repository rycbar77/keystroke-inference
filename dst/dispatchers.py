import warnings

import numpy as np
from matplotlib import pyplot as plt

from dst.libraries import al

warnings.filterwarnings("ignore")


def dispatcher(in_queue, out_queue, display_queue, config, interact=False):
    for data in iter(in_queue.get, None):
        rem = len(data) % 441
        data = np.array(data[:len(data) - rem])
        minimum_interval = config['dispatcher_min_interval']
        sample_length = (44100 * config['dispatcher_window_size']) // 1000

        peaks = []
        for x in range(0, len(data) - 440):
            peaks.append(np.sum(np.absolute(np.fft.fft(data[x:x + 440]))))
        peaks = np.array(peaks)
        threshold = config['dispatcher_threshold']
        tau = np.percentile(peaks, config['dispatcher_threshold'])
        if interact:
            while threshold != -1:
                tau = np.percentile(peaks, threshold)
                plt.plot(peaks)
                plt.axhline(y=tau, ls="-", c="red")
                plt.show()
                threshold = float(input("Choose a threshold in [0,100], input nothing or -1 to confirm.\n")) or -1
                if threshold > 100 or (threshold < 0 and threshold != -1):
                    raise Exception("Invalid threshold")
        x = 0
        events = []
        step = config['dispatcher_step_size']
        past_x = - minimum_interval - step
        idx = 0
        while x < peaks.size:
            if peaks[x] >= tau:
                if x - past_x >= minimum_interval:
                    keypress = al.normalize(data[x:x + sample_length])
                    past_x = x
                    out_queue.put([idx, keypress])
                    idx += 1
                    events.append(keypress)
                x = past_x + minimum_interval
            else:
                x += step

        display_queue.put(len(events))

    for _x in range(config['workers']):
        out_queue.put((-1, None))
