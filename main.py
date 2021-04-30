import argparse

import config
from utils.dispatchers import dispatcher
from utils.listeners import wav_file
from utils.output import console
from utils.predict import predict

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", "-t", type=str)
    parser.add_argument("--model", "-m", action='append', type=str, required=True)
    parser.add_argument("--interactive", "-i", type=bool, default=True)

    args = parser.parse_args()
    pipeline_list = []
    output_list = []

    out = wav_file(args.target)
    peaks = dispatcher(out, args.interactive)

    for model in args.model:
        res = predict(model, peaks, config.n_predictions)
        if 'svm' not in model:
            console(res)
