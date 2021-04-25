import warnings

from dst.libraries import al

warnings.filterwarnings("ignore")


def wav_file(in_file, out_queue):
    _, mono = al.load(in_file)
    out_queue.put(list(mono))
    out_queue.put(None)

# see keylogger.py
