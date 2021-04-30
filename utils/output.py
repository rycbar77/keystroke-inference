import os

import numpy as np
from wordfreq import zipf_frequency
from config import n_predictions

def dictionary_filter(guesses, wl, nums=50):
    wl = [x for x in wl if len(x) == len(guesses)]

    def freq(x):
        return zipf_frequency(x, 'en')

    def score(word):
        penalty = 0
        for guess, letter in zip(guesses, word):
            if letter in guess:
                penalty += guess.index(letter)
            else:
                penalty += n_predictions
        return penalty

    wls = sorted([(x, score(x) - freq(x) * 0.8) for x in wl], key=lambda _x: _x[1])

    return wls[:nums]


def dictionary_interactive(pred):
    ans = input("Check Check [Y/n] ")
    if ans == 'n':
        return
    separators = input("Which are the word separators? (separated with spaces): ").split(" ")

    spaces = [int(i) for i in separators if i != '']
    spaces.append(len(pred))

    last_idx = 0

    dictionaries = []
    for r, d, fs in os.walk('../dictionaries/'):
        for fn in fs:
            dictionaries.append(os.path.abspath(os.path.join(r, fn)))
    if len(dictionaries) == 0:
        print("No dictionaries available!")
        return
    print("Available dictionaries:")
    for i, d in enumerate(dictionaries):
        print("{} - {}".format(i, d))
    ans = input("Select dictionary number ([0]): ") or 0

    wl = np.loadtxt(dictionaries[int(ans)], dtype=str)
    for space in spaces:
        word_guesses = pred[last_idx:space]
        print("Word From Character {} to {}".format(last_idx, space))
        print(dictionary_filter(word_guesses, wl, 30))
        print("")
        last_idx = space + 1


def console(in_queue):
    output = []
    for idx, pred in in_queue:
        output.append(pred)

    print("predictions")
    print("")
    for i, p in enumerate(output):
        print("{} - {}".format(i, p))
    dictionary_interactive(output)
