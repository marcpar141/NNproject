from numpy import zeros, min, max, float32
import get_bin


def parse_line(path):
    """Parse an ndjson line and return ink (as np array) and classname."""
    sample = get_bin.get_bin(path).data
    class_name = [letter for letter in path]
    class_name = class_name[:len(class_name)-4]
    class_name = ''.join(class_name[7:])
    inkarray = sample["image"]
    stroke_lengths = [len(stroke[0]) for stroke in inkarray]
    total_points = sum(stroke_lengths)
    np_ink = zeros((total_points, 3), dtype=float32)
    current_t = 0
    for stroke in inkarray:
        for i in [0, 1]:
            np_ink[current_t:(current_t + len(stroke[0])), i] = stroke[i]
        current_t += len(stroke[0])
        np_ink[current_t - 1, 2] = 1  # stroke_end
    # Preprocessing.
    # 1. Size normalization.
    lower = min(np_ink[:, 0:2], axis=0)
    upper = max(np_ink[:, 0:2], axis=0)
    scale = upper - lower
    scale[scale == 0] = 1
    np_ink[:, 0:2] = (np_ink[:, 0:2] - lower) / scale

    # 2. Compute deltas.
    np_ink[1:, 0:2] -= np_ink[0:-1, 0:2]
    np_ink = np_ink[1:, :]
    # you can give axis attribute if you wanna squeeze in specific dimension
    return np_ink, class_name
