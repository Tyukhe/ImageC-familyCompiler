from PIL import Image, ImageDraw
from tree import Branch
from blocks import *


class Scheme:
    def __init__(self, name, tree, font, glob=None):
        self.types = ["int", "long", "float", "char"]

        self.name = f'{name}.png'
        self.font = font

        maxString = ''
        for i in tree:
            if len(str(i.item)) > len(maxString):
                maxString = str(i.item)
        self.w, self.h = self.font.getmask(maxString).getbbox()[2], self.font.getmask(maxString).getbbox()[3]
        self.b = self.w * 1.25 # TODO подобрать значение
        self.a = self.b / 1.5

        self.tree = tree
        for i in tree:
            i.item.set_ab((self.a, self.b))
        # Startend("Конец", (self.a, self.b), self.font)

    def render(self):
        cellHeight = self.a + self.w / 4  # TODO Подобрать значения
        cellWith = self.b + self.w / 4

        matrix, down = self.tree.get_matrix((0, 0))
        size = (int(matrix.column * cellWith), int(matrix.row * cellHeight))

        img = Image.new('RGB', size, 'white')
        img.save(self.name)
        img = Image.open(self.name)

        holst = ImageDraw.Draw(img)

        for key in matrix.keys():
            matrix[key].draw((key[0] * cellWith + cellWith / 2, key[1] * cellHeight + cellHeight / 2), holst)
            matrix[key].draw_arrows((key[0] * cellWith + cellWith / 2, key[1] * cellHeight + cellHeight / 2), (cellWith, cellHeight), holst)
        img.save(self.name)
        img.show()