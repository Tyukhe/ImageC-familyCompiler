from PIL import Image, ImageDraw
from tree import Branch
from blocks import *


class Scheme:
    def __init__(self, name, code, font, glob=None):
        self.types = ["int", "long", "float", "char"]

        self.name = f'{name}.png'
        self.font = font

        self.maxString = self.get_max(code)
        self.w, self.h = self.font.getmask(self.maxString).getbbox()[2], self.font.getmask(self.maxString).getbbox()[3]
        self.b = self.w * 1.25 # TODO подобрать значение
        self.a = self.b / 1.5

        self.tree = Branch(Startend("Начало", (self.a, self.b), self.font), self.make_blocks(code))
        # Startend("Конец", (self.a, self.b), self.font)

    def make_blocks(self, code):
        res = []
        for i in code:
            if isinstance(i, list):
                res.append(self.make_blocks(i))
            else:
                res.append(Block(i, (self.a, self.b), self.font))
        return res

    def get_max(self, arr):
        res = ""
        for i in arr:
            if type(i) is list:
                localMax = self.get_max(i)
                if len(res) < len(localMax):
                    res = localMax
            else:
                if len(res) < len(i):
                    res = i
        return res

    def render(self):
        cellHeight = self.a + self.w / 4  # TODO Подобрать значения
        cellWith = self.b + self.w / 4

        matrix = self.tree.get_matrix((0, 0))
        size = (int(matrix.row * cellWith), int(matrix.column * cellHeight))

        img = Image.new('RGB', size, 'white')
        img.save(self.name)
        img = Image.open(self.name)

        holst = ImageDraw.Draw(img)

        for key in matrix.keys():
            matrix[key].item.draw((key[0] * cellWith + cellWith / 2, key[1] * cellHeight + cellHeight / 2), holst)
        img.save(self.name)
        img.show()