import argparse

from config import dispatcher_threshold
from utils.dispatchers import dispatcher
from utils.listeners import wav_file
from utils.output import console
from utils.predict import predict

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", "-t", type=str)
    parser.add_argument("--model", "-m", action='append', type=str, required=True)
    parser.add_argument("--interactive", "-i", type=bool, default=True)
    parser.add_argument("--dispatcher_threshold", type=float, default=dispatcher_threshold)
    parser.add_argument("--n_predictions", "-n", type=int, default=15)

    args = parser.parse_args()
    dispatcher_threshold = args.dispatcher_threshold
    n_predictions = args.n_predictions
    pipeline_list = []
    output_list = []

    out = wav_file(args.target)
    iq = dispatcher(out, args.interactive)

    for model in args.model:
        rq = predict(model, iq, args.n_predictions)
        if 'svm' not in model:
            console(rq)
