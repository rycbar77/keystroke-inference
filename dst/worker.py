import joblib


def worker(model, in_queue, out_queue, num_of_pred):
    clf = joblib.load(model)
    while True:
        if in_queue.empty():
            break
        idx, sample = in_queue.get()
        if 'svm' in model:
            prediction = "".join(clf.predict(sample.reshape(1, -1)))
            print(prediction)
        else:
            prediction = clf.predict_proba(sample.reshape(1, -1))[0]
            values = [x[0] for x in
                      sorted([(clf.classes_[x], val) for x, val in enumerate(prediction) if val != 0.0],
                             key=lambda _x: _x[1], reverse=True)]
            out_queue.put((idx, values[:num_of_pred]))
    return
