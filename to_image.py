import get_bin
import numpy as np
import turtle


class to_image:
    def __init__(self, class_name):
        self.class_name = class_name
        self.data = np.array(get_bin.get_bin("D://db/{}.bin".format(self.class_name)).data["image"])
        self.my_array = []
        self._fill()

    def _fill(self):
        i = 0
        while i < len(self.data):
            strokes = []
            lst = list(self.data[i])
            for x in range(len(lst[0])):
                strokes.append([lst[0][x], lst[1][x]])

            self.my_array.append(strokes)
            i += 1

    def _draw(self):
        s = turtle.Screen()
        t = turtle.Turtle()

        for j in self.my_array:
            V_prev = [-1, -1]
            print(j)
            for i, x in enumerate(j):
                x = list(x)
                if i - 1 == len(j):
                    break

                V = x
                V[1] = V[1] * (-1)

                if i == 0:
                    t.penup()
                    t.goto(V)
                else:
                    t.pendown()
                    t.goto(V)

                V_prev = V

    def show(self):
        self._draw()
        turtle.done()


if __name__ == "__main__":
    img = to_image("car")
    img.show()
