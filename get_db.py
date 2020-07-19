import struct
import random
from struct import unpack


class get_db:
    def __init__(self, path):
        self.path = path  # path for data like "ant.bin"
        self.data = self.show(self.path)

    @staticmethod
    def unpack_drawing(file_handle):
        key_id, = unpack('Q', file_handle.read(8))
        country_code, = unpack('2s', file_handle.read(2))
        recognized, = unpack('b', file_handle.read(1))
        timestamp, = unpack('I', file_handle.read(4))
        n_strokes, = unpack('H', file_handle.read(2))
        image = []
        for i in range(n_strokes):
            n_points, = unpack('H', file_handle.read(2))
            fmt = str(n_points) + 'B'
            x = unpack(fmt, file_handle.read(n_points))
            y = unpack(fmt, file_handle.read(n_points))
            image.append((x, y))

        return {
            'key_id': key_id,
            'country_code': country_code,
            'recognized': recognized,
            'timestamp': timestamp,
            'image': image
        }

    def unpack_drawings(self, filename):
        with open(filename, 'rb') as f:
            while True:
                try:
                    yield self.unpack_drawing(f)
                except struct.error:
                    break

    def show(self, path):
        max_i = 0
        for drawing in self.unpack_drawings(path):
            max_i += 1
        i = 0
        index = random.randint(1, max_i)
        for drawing in self.unpack_drawings(path):
            i += 1
            if i == index:
                return drawing
