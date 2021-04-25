import argparse
import os
from queue import Queue

import joblib
import numpy as np
from sklearn.feature_selection import RFECV
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import LinearSVC

from config import *
from dst.dispatchers import dispatcher
from dst.listeners import wav_file
from dst.miners import MFCC

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('training_data', nargs='+', type=str)
    parser.add_argument('output_file', type=str)
    parser.add_argument('--folds', type=int, default=5)
    args = parser.parse_args()

    files_to_mine = {}
    mined_files = {}
    wav_files = []
    label_files = []
    press_files = []


    def add_file(file):
        ext = os.path.splitext(file)[-1]
        if ext == '.wav':
            wav_files.append(file)
        elif ext == '.press':
            press_files.append(file)
        elif ext == '.txt':
            label_files.append(file)


    for f_name in args.training_data:
        f = os.path.abspath(f_name)
        if os.path.isfile(f):
            add_file(f)
        elif os.path.isdir(f):
            for r, d, fs in os.walk(f):
                for fn in fs:
                    ff = os.path.abspath(os.path.join(r, fn))
                    add_file(ff)

    wav_files_map = {}
    for f in wav_files:
        basename = os.path.splitext(os.path.basename(f))[0]
        if os.path.splitext(f)[0] + '.press' not in press_files:
            wav_files_map[f] = None
            for l_f in label_files:
                if os.path.splitext(os.path.basename(l_f))[0] == basename:
                    wav_files_map[f] = l_f

    press_files_map = {}
    for f in press_files:
        basename = os.path.splitext(os.path.basename(f))[0]
        press_files_map[f] = None
        for l_f in label_files:
            if os.path.splitext(os.path.basename(l_f))[0] == basename:
                press_files_map[f] = l_f

    mismatches = [x for x, y in wav_files_map.items() if y is None] + [x for x, y in press_files_map.items() if
                                                                       y is None]
    if len(mismatches) != 0:
        print("Mismatch")
        for f in mismatches:
            print(f)
        exit()

    print("{} files processed".format(len(press_files)))
    print("{} files to process".format(len(wav_files) - len(press_files)))
    f_X, f_y = [], []
    error_queue = []

    events_queue = []
    for i, (wav, label_file) in iter(enumerate(wav_files_map.items())):
        print("Processing file #{}".format(i + 1))
        lq = Queue()
        wav_file(wav, lq)

        oq, dq = Queue(), Queue()
        dispatcher(lq, oq, dq, CONFIG)

        y = np.loadtxt(label_file, dtype=str, delimiter='\n')
        events_queue.append((wav, y, oq, dq))

        for _wav, y, oq, dq in events_queue:
            if dq.empty():
                break
            n_res = dq.get()
            if not len(y.shape):
                y = y.reshape(0)
            if n_res != len(y):
                error_queue.append((_wav, n_res, len(y)))
            else:
                X = []
                while len(X) < len(y):
                    X.append(oq.get())
                np.savetxt(os.path.splitext(_wav)[0] + '.press', X)
                f_X.extend(X)
                f_y.extend(y)

    if len(error_queue) != 0:
        print("wrong number of key presses found:")
        for f, found, expected in error_queue:
            print("{} - found {}, expected {}".format(f, found, expected))
        exit()

    for press_file, label_file in press_files_map.items():
        f_X.extend(np.loadtxt(press_file))
        f_y.extend(np.loadtxt(label_file, dtype=str, delimiter='\n'))
    f_X, f_y = np.array(f_X), np.array(f_y)
    # push_peak_zise = f_X.shape[1]
    # numCharacters = len(set(f_y))
    pipeline = [('MFCC', MFCC()), ('Scaler', MinMaxScaler())]
    # classifier = LogisticRegression()
    classifier = LinearSVC()
    # classifier = MLPRegressor(hidden_layer_sizes=(150, 100))
    pipeline.append(('Feature Selection', RFECV(classifier, step=f_X.shape[1] / 10, cv=args.folds, verbose=0)))
    pipeline.append(('Classifier', classifier))
    clf = Pipeline(pipeline)
    # clf = classifier
    print("Learning")
    # model = train(f_X, f_y, push_peak_zise, numCharacters)
    clf.fit(f_X, f_y)
    print("Completed!")
    # joblib.dump(model, args.output_file)
    joblib.dump(clf, args.output_file)
    print("Acc:")
    print(np.mean(cross_val_score(clf, f_X, f_y, cv=args.folds + 1)))
