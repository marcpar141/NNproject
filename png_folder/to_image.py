import get_bin
import numpy as np
import turtle
from PIL import Image
import os, glob
import shutil


class to_image:
    def __init__(self, class_name):
        self.class_name = class_name
        self.data = np.array(get_bin.get_bin("D://db/{}.bin".format(self.class_name)).data["image"])
        self.my_array = []
        self._fill()
        self.index = 0

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
        self.s = turtle.Screen()
        self.s.colormode(1)
        t = turtle.Turtle()
        t.hideturtle()

        for j in self.my_array:
            V_prev = [-1, -1]
            print(j)
            # t.pencolor(randint(0, 255), randint(0, 255), randint(0, 255))
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

    def save(self):
        self._chop_blank()

    def _to_ps(self):
        self._draw()
        self.s = self.s.getcanvas().postscript(file=''.join([self.class_name, '.ps']))

    def _conv_ps_png(self):
        self._to_ps()
        list_ps = glob.glob('*.ps')
        for file in list_ps:
            root = file[:-3]
            pngfile = ''.join([root, ".png"])
            os.system(''.join(['magick', ' ', 'convert ', file, " -strip", " ", pngfile]))

    def _chop_blank(self):
        self._conv_ps_png()
        pil_img = Image.open('car.png')
        pil_img.getbbox()
        print(pil_img.size)
        cropped_img = pil_img.crop(pil_img.getbbox())
        np_img = np.array(cropped_img)
        img = Image.fromarray(np_img)
        scaled_img = img.resize((32, 32))
        if os.path.exists("{}.png".format(self.class_name)):
            scaled_img.save("{}{}.png".format(self.class_name, self.index, interpolation="nearest"))
            self.index += 1
        else:
            scaled_img.save("{}.png".format(self.class_name), interpolation="nearest")


class all_to_image:
    def __init__(self, class_name):
        self.class_name = class_name
        self.my_array = []
        self.index = 0
        self._chop_all_blank()

    def _draw(self):
        self.s = turtle.Screen()
        self.s.colormode(1)
        t = turtle.Turtle()
        t.hideturtle()

        for j in self.my_array:
            V_prev = [-1, -1]
            print(j)
            # t.pencolor(randint(0, 255), randint(0, 255), randint(0, 255))
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

    def _to_ps(self):
        self._draw()
        self.s = self.s.getcanvas().postscript(file="{}{}.ps".format(self.class_name, self.index))
        os.listdir("D://Repos/NNproject/")
        shutil.move("D://Repos/NNproject/{}{}.ps".format(self.class_name, self.index), "D://Repos/NNproject/ps_folder")
        os.remove("D://Repos/NNproject/{}{}.ps".format(self.class_name, self.index))

    def _ps_everything(self):
        self.data = get_bin.get_bin("D://db/{}.bin".format(self.class_name)).return_all()
        for drawing in self.data:
            self._to_ps()
            self.index += 1

    def _chop_all_blank(self):
        self._conv_all_ps_png()
        for drawing in
            pil_img = Image.open('car.png')
        np_img = np.array(pil_img)
        idx0 = np.argwhere(np.all(np_img)[..., :] == 0, axis=0)
        idx255 = np.argwhere(np.all(np_img[..., :] == 255, axis=0))

        print(np_img, np_img.shape)

    @staticmethod
    def _conv_all_ps_png():
        list_ps = glob.glob('*.ps')
        for file in list_ps:
            root = file[:-3]
            pngfile = ''.join([root, ".png"])
            os.system(''.join(['magick', ' ', 'convert ', file, " ", pngfile]))


if __name__ == "__main__":
    all_img = all_to_image("car")
    # img = to_image("car")
    # img.save()
