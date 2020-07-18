#!/usr/bin/env pypy
import struct
from struct import unpack


class get_db:
    def __init__(self, name, data_type):
        self.data_type = data_type # Data types are enumerate in method unpack_drawing inside of return
        self.name = name # Name of data
        self.show(self.name, self.data_type)

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

    def show(self, name, data_type):
        for drawing in self.unpack_drawings(name):
            # do something with the drawing
            print(drawing[data_type])
