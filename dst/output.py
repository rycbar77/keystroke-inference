from dst.libraries.dictionary_filter import dictionary_interactive


def console(in_queue, config):
    output = []
    while True:
        if in_queue.empty():
            break
        idx, pred = in_queue.get()
        output.append(pred)

    print("predictions")
    print("")
    for i, p in enumerate(output):
        print("{} - {}".format(i, p))
    dictionary_interactive(output, config)
