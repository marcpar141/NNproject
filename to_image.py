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
        print(self.data)
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
            print(strokes)

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
        print(np_img)
        img = Image.fromarray(np_img)
        scaled_img = img.resize((32, 32))
        if os.path.exists("{}.png".format(self.class_name)):
            scaled_img.save("{}{}.png".format(self.class_name, self.index, interpolation="nearest"))
            self.index += 1
        else:
            scaled_img.save("{}.png".format(self.class_name), interpolation="nearest")


class all_to_image:
    def __init__(self, class_name, how_many=10):
        self.how_many = how_many
        self.class_name = class_name
        self.my_array = []
        self.index = 0
        self._ps_everything()
        self._chop_all_blank()

    def _fill(self):  # Zrób ograniczenie oraz żeby żółw rysował
        i = 0
        while i < len(self.data):
            strokes = []
            lst = list(self.data[i])
            for x in range(len(lst[0])):
                strokes.append([lst[0][x], lst[1][x]])

            self.my_array.append(strokes)
            i += 1
            print(strokes)

    def _draw(self):
        self.s = turtle.Screen()
        self.s.colormode(1)
        self.t = turtle.Turtle()
        self.t.speed('fastest')
        self.t.hideturtle()

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
                    self.t.penup()
                    self.t.goto(V)
                else:
                    self.t.pendown()
                    self.t.goto(V)

                V_prev = V


    def _to_ps(self):
        self._fill()
        self._draw()
        self.my_array = []
        self.s = self.s.getcanvas().postscript(file="{}{}.ps".format(self.class_name, self.index))
        self.t.clear()
        shutil.move("D://Repos/NNproject/{}{}.ps".format(self.class_name, self.index), "D://Repos/NNproject/ps_folder")

    def _ps_everything(self):
        self.data = get_bin.get_bin("D://db/{}.bin".format(self.class_name)).return_all()
        self.clear_ps()
        for i, drawing in enumerate(self.data):
            if i < self.how_many:
                print(drawing)
                self.data = drawing
                self._to_ps()
                self.index += 1
            else:
                break

    def _chop_all_blank(self):
        self._conv_all_ps_png()
        self.index = 0
        for drawing in os.listdir("D://Repos/NNproject/png_folder"):
            pil_img = Image.open(drawing)
            pil_img.getbbox()
            print(pil_img.size)
            cropped_img = pil_img.crop(pil_img.getbbox())
            np_img = np.array(cropped_img)
            print(np_img)
            img = Image.fromarray(np_img)
            scaled_img = img.resize((32, 32))
            if os.path.exists("{}.png".format(self.class_name)):
                scaled_img.save("{}{}.png".format(self.class_name, self.index, interpolation="nearest"))
                self.index += 1
            else:
                scaled_img.save("{}.png".format(self.class_name), interpolation="nearest")

    @staticmethod
    def _conv_all_ps_png():
        list_ps = glob.glob('ps_folder/*.ps')
        for file in list_ps:
            root = file[:-3]
            pngfile = ''.join([root, ".png"])
            os.system(''.join(['magick', ' ', 'convert ', file, " ", pngfile]))
        png_in_ps = glob.glob('ps_folder/*.png')
        for file in png_in_ps:
            shutil.move("D://Repos/NNproject/{}".format(file),
                        "D://Repos/NNproject/png_folder")

    @staticmethod
    def clear_ps():
        for filename in os.listdir("D://Repos/NNproject/ps_folder/"):
            filepath = os.path.join("D://Repos/NNproject/ps_folder/", filename)
            os.unlink(filepath)


if __name__ == "__main__":
    img = all_to_image("car")
#    img = to_image("car")
#    img.save()
