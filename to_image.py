import get_bin
import numpy as np
import turtle
from PIL import Image
import os, glob
import shutil


class to_image:
    def __init__(self, class_name, chosen_type="png"):
        self.chosen_type = chosen_type
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

    def _conv_ps(self):
        self._to_ps()
        list_ps = glob.glob('*.ps')
        for file in list_ps:
            root = file[:-3]
            pngfile = ''.join([root, ".{}".format(self.chosen_type)])
            os.system(''.join(['magick', ' ', 'convert ', file, " -strip", " ", pngfile]))

    def _chop_blank(self):
        self._conv_ps()
        pil_img = Image.open('car.{}'.format(self.chosen_type))
        pil_img.getbbox()
        print(pil_img.size)
        cropped_img = pil_img.crop(pil_img.getbbox())
        # np_img = np.array(cropped_img)
        # print(np_img)
        # img = Image.fromarray(np_img)
        scaled_img = cropped_img.resize((32, 32))
        if os.path.exists("{}.{}}".format(self.class_name, self.chosen_type)):
            scaled_img.save("{}{}.{}".format(self.class_name, self.index, self.chosen_type), interpolation="nearest")
            self.index += 1
        else:
            scaled_img.save("{}.{}".format(self.class_name, self.chosen_type), interpolation="nearest")


class all_to_image:
    """
    Tanslating chosen number of pictures from vector array to chosen image type( between png and bmp )

    """

    def __init__(self, class_name, chosen_type="png"
                 , lower_bound=0, higher_bound=100):

        self.lower_bound = lower_bound
        self.higher_bound = higher_bound
        self.chosen_type = chosen_type
        self.class_name = class_name
        self.my_array = []
        self.index = 0
        self.current_dir = os.getcwd()
        self.clear_ps()
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
        self.s.tracer(0, 0)
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
            self.s.update()

    def _to_ps(self):
        self._fill()
        self._draw()
        self.my_array = []
        self.s = self.s.getcanvas().postscript(file="{}{}.ps".format(self.class_name, self.index))
        self.t.clear()
        shutil.move("".join([self.current_dir, "/", self.class_name, str(self.index), ".ps"]),
                    "".join([self.current_dir, "/ps_folder"]))

    def _ps_everything(self):
        self.data = get_bin.get_bin("D://db/{}.bin".format(self.class_name)).return_all()
        self.clear_ps()
        for i, drawing in enumerate(self.data):
            if i >= self.lower_bound:
                if i < self.higher_bound:
                    print(drawing)
                    self.data = drawing
                    self._to_ps()
                    self.index += 1
                else:
                    break

    def _chop_all_blank(self):
        self._conv_all_ps_png()
        self.index = self.lower_bound
        for drawing in os.listdir("pic_folder/"):
            pil_img = Image.open("".join([self.current_dir, "/pic_folder/", drawing]))
            pil_img.getbbox()
            print(pil_img.size)
            cropped_img = pil_img.crop(pil_img.getbbox())
            # print(cropped_img)
            # np_img = np.array(cropped_img)
            # print(np_img)
            # img = Image.fromarray(np_img)
            scaled_img = cropped_img.resize((32, 32))
            scaled_img.save("{}{}.{}".format(self.class_name, self.index, self.chosen_type)
                            , interpolation="nearest")
            self.index += 1

        self.clear_pic()
        for file in os.listdir(self.current_dir):
            if file.endswith(".{}".format(self.chosen_type)):
                shutil.move("".join([self.current_dir, "/", file]),
                            "".join([self.current_dir, "/pic_folder/", file]))

    def _conv_all_ps_png(self):
        list_ps = os.listdir('ps_folder/')
        print(list_ps)
        for file in list_ps:
            root = file[:-3]
            pngfile = ''.join([root, ".", self.chosen_type])
            os.system(''.join(['magick', ' ', 'convert ', "ps_folder/", file, " ", pngfile]))
            shutil.move("".join([self.current_dir, "/", pngfile]),
                        "".join([self.current_dir, "/pic_folder/", pngfile]))
        self.clear_ps()
        self.clear_root()

    def clear_ps(self):
        for filename in os.listdir("".join([self.current_dir, "/ps_folder"])):
            filepath = os.path.join("".join([self.current_dir, "/ps_folder/", filename]))
            os.unlink(filepath)

    def clear_pic(self):
        for filename in os.listdir("".join([self.current_dir, "/pic_folder"])):
            filepath = os.path.join("".join([self.current_dir, "/pic_folder/", filename]))
            os.unlink(filepath)

    def clear_root(self):
        for filename in os.listdir(self.current_dir):
            if filename.endswith(".png"):
                filepath = os.path.join("".join([self.current_dir, "/", filename]))
                os.unlink(filepath)


if __name__ == "__main__":
    img = all_to_image("car", lower_bound=0, higher_bound=150)

#    img = to_image("car")
#    img.save()
