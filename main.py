import argparse
from queue import Queue

from config import *
from dst.dispatchers import dispatcher
from dst.listeners import wav_file
from dst.output import console
from dst.worker import worker

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", "-t", type=str)
    parser.add_argument("--model", "-m", action='append', type=str, required=True)
    parser.add_argument("--interactive", "-i", type=bool, default=True)
    parser.add_argument("--dispatcher_threshold", type=float, default=CONFIG['dispatcher_threshold'])
    parser.add_argument("--n_predictions", "-n", type=int, default=15)

    args = parser.parse_args()

    for key, val in vars(args).items():
        CONFIG[key] = val

    pipeline_list = []
    output_list = []

    lq = Queue()
    wav_file(args.target, lq)
    oq, dq = Queue(), Queue()
    dispatcher(lq, oq, dq, CONFIG, args.interactive)

    for p_idx, model in enumerate(args.model):
        iq, rq = Queue(), Queue()
        while True:
            res = oq.get()
            if res[0] == -1:
                break
            iq.put(res)

        worker(model, iq, rq, args.n_predictions)
        if 'svm' not in model:
            console(rq, CONFIG)
