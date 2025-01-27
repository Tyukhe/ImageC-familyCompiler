from PIL import Image, ImageDraw

class Block:
    def __init__(self, text, ab, font):
        self.text = text
        self.font = font

        self.w, self.h = self.font.getmask(self.text).getbbox()[2], self.font.getmask(self.text).getbbox()[3]
        self.a, self.b = ab

    def __str__(self):
        return self.text

    def draw_arrows(self, xy, cell, holst, dirs=(True, False, False, True)):
        x, y = xy
        cx, cy = cell
        if dirs[0]:
            holst.line((x, y - cy / 2, x, y - self.a / 2), 'black', 3)
            holst.line((x, y - self.a / 2, x + self.a / 30, y - self.a / 30 * 17), 'black', 3)
            holst.line((x, y - self.a / 2, x - self.a / 30, y - self.a / 30 * 17), 'black', 3)
        if dirs[1]:
            holst.line((x - cx / 2, y, x - self.b / 2, y), 'black', 3)
        if dirs[2]:
            holst.line((x + self.b / 2, y, x + cx / 2, y), 'black', 3)
        if dirs[3]:
            holst.line((x, y + self.a / 2, x, y + cy / 2), 'black', 3)

    def draw(self, xy:tuple, holst:ImageDraw):
        x, y = xy
        holst.text((x - self.w / 2, y - self.h / 2), self.text, fill='black', font=self.font)
        holst.rectangle((x - self.b / 2, y - self.a / 2, x + self.b / 2, y + self.a / 2), outline="black", width=3)


class Startend(Block):
    def draw(self, xy, holst):
        x, y = xy
        holst.text((x - self.w / 2, y - self.h / 2), self.text, fill='black', font=self.font)
        holst.line((x + self.b / 2 - self.a / 4, y + self.a / 4, x - self.b / 2 + self.a / 4, y + self.a / 4), 'black', 3)
        holst.line((x + self.b / 2 - self.a / 4, y - self.a / 4, x - self.b / 2 + self.a / 4, y - self.a / 4), 'black', 3)
        holst.arc((x + self.b / 2 - self.a / 2, y - self.a / 4, x + self.b / 2, y + self.a / 4), -90, 90, 'black', 3)
        holst.arc((x - self.b / 2, y - self.a / 4, x - self.b / 2 + self.a / 2, y + self.a / 4), 90, -90, 'black', 3)


class If(Block):
    def draw(self, xy, holst):
        x, y = xy
        holst.text((x - self.w / 2, y - self.h / 2), self.text, fill='black', font=self.font)
        holst.line((x + self.b / 2, y, x, y - self.a / 2), 'black', 3)
        holst.line((x, y - self.a / 2, x - self.b / 2, y), 'black', 3)
        holst.line((x - self.b / 2, y, x, y + self.a / 2), 'black', 3)
        holst.line((x, y + self.a / 2, x + self.b / 2, y), 'black', 3)

        holst.text((x + self.b / 2 + self.h * 0.5, y - self.h * 1.5), "Да", fill='black', font=self.font)
        holst.text((x + self.h * 0.5, y + self.a / 2), "Нет", fill='black', font=self.font)


class For(Block):
    def draw(self, xy, holst):
        x, y = xy
        holst.text((x - self.w / 2, y - self.h / 2), self.text, fill='black', font=self.font)
        holst.line((x + self.b / 2, y, x + self.a / 2, y - self.a / 2), 'black', 3)
        holst.line((x + self.a / 2, y - self.a / 2, x - self.a / 2, y - self.a / 2), 'black', 3)
        holst.line((x - self.a / 2, y - self.a / 2, x - self.b / 2, y), 'black', 3)
        holst.line((x - self.b / 2, y, x - self.a / 2, y + self.a / 2), 'black', 3)
        holst.line((x - self.a / 2, y + self.a / 2, x + self.a / 2, y + self.a / 2), 'black', 3)
        holst.line((x + self.a / 2, y + self.a / 2, x + self.b / 2, y), 'black', 3)


class Func(Block):
    def draw(self, xy, holst):
        x, y = xy
        holst.text((x - self.w / 2, y - self.h / 2), self.text, fill='black', font=self.font)
        holst.rectangle((x - self.b / 2, y - self.a / 2, x + self.b / 2, y + self.a / 2), outline="black", width=3)
        holst.line((x + self.b / 2 - self.a * 0.15, y - self.a / 2, x + self.b / 2 - self.a * 0.15, y + self.a / 2), 'black', 3)
        holst.line((x - self.b / 2 + self.a * 0.15, y - self.a / 2, x - self.b / 2 + self.a * 0.15, y + self.a / 2), 'black', 3)


class Inout(Block):
    def draw(self, xy, holst):
        x, y = xy
        holst.text((x - self.w / 2, y - self.h / 2), self.text, fill='black', font=self.font)
        holst.line((x + self.b / 2 - self.a * 0.25, y + self.a / 2, x + self.b / 2, y - self.a / 2), 'black', 3)
        holst.line((x + self.b / 2, y - self.a / 2, x - self.b / 2 + self.a * 0.25, y - self.a / 2), 'black', 3)
        holst.line((x - self.b / 2 + self.a * 0.25, y - self.a / 2, x - self.b / 2, y + self.a / 2), 'black', 3)
        holst.line((x - self.b / 2, y + self.a / 2, x + self.b / 2 - self.a * 0.25, y + self.a / 2), 'black', 3)


2