import numpy as np
import get_db
import matplotlib.pyplot as plt


def parse_line(path):
    """Parse an ndjson line and return ink (as np array) and classname."""
    sample = get_db.get_db(path).data
    class_name = [letter for letter in path]
    class_name = class_name[:len(class_name)-4]
    class_name = ''.join(class_name[3:])
    inkarray = sample["image"]
    stroke_lengths = [len(stroke[0]) for stroke in inkarray]
    total_points = sum(stroke_lengths)
    np_ink = np.zeros((total_points, 3), dtype=np.float32)
    current_t = 0
    for stroke in inkarray:
        for i in [0, 1]:
            np_ink[current_t:(current_t + len(stroke[0])), i] = stroke[i]
        current_t += len(stroke[0])
        np_ink[current_t - 1, 2] = 1  # stroke_end
    # Preprocessing.
    # 1. Size normalization.
    lower = np.min(np_ink[:, 0:2], axis=0)
    upper = np.max(np_ink[:, 0:2], axis=0)
    scale = upper - lower
    scale[scale == 0] = 1
    np_ink[:, 0:2] = (np_ink[:, 0:2] - lower) / scale

    # 2. Compute deltas.
    np_ink[1:, 0:2] -= np_ink[0:-1, 0:2]
    np_ink = np_ink[1:, :]
    arr_ = np.squeeze(np_ink)  # you can give axis attribute if you wanna squeeze in specific dimension
    plt.imshow(arr_)
    plt.show()
    return np_ink, class_name


data = parse_line("db/airplane.bin")
print(data)