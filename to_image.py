import get_bin
import numpy as np
import matplotlib.pyplot as plt


class to_image:
    def __init__(self):
        self.data = np.array(get_bin.get_bin("D://db/car.bin").data["image"])
        self.my_array = []
        self._fill()

    def _fill(self):
        for i in self.data:
            lst = list(i)
            for x in range(len(lst[0])):
                self.my_array.append([lst[0][x], lst[1][x]])

    def _draw(self):
        for i in range(len(self.my_array) + 1):
            if i == len(self.my_array):
                break
            V1 = self.my_array[i - 1]
            V2 = self.my_array[i]

            plt.quiver(V1[0], V1[1] * (-1), V2[0], V2[1] * (-1))

    def show(self):
        self._draw()
        plt.show()

    def save(self):
        self._draw()
        plt.imsave("img.png")


# TEST
"""
if __name__ == "__main__":
    img = to_image()
    img.show()
    img.show()
    img.save()
"""
