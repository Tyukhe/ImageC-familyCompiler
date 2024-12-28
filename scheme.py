from PIL import Image, ImageDraw
from matrix import Matrix


class Block:
    def __init__(self, text, ab, font, uid=(-1, -1)):
        self.text = text
        self.font = font
        self.uid = uid

        self.w, self.h = self.font.getmask(self.text).getbbox()[2], self.font.getmask(self.text).getbbox()[3]
        self.a, self.b = ab

    def __str__(self):
        return str(self.text)

    def draw(self, xy:tuple, holst:ImageDraw):
        x, y = xy
        holst.text((x - self.w / 2, y - self.h / 2), self.text, fill='black', font=self.font)
        holst.rectangle((x - self.b / 2, y - self.a / 2, x + self.b / 2, y + self.a / 2), outline="black", width=3)


class Startend(Block):
    def draw(self, xy, holst):
        x, y = xy
        print()
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


class Scheme:
    def __init__(self, name, code, font, glob=None):
        self.name = f'{name}.png'
        self.code = code
        self.font = font
        self.maxString = self.get_max(self.code)

        self.w, self.h = self.font.getmask(self.maxString).getbbox()[2], self.font.getmask(self.maxString).getbbox()[3]
        self.b = self.w * 1.1 # TODO подобрать значение
        self.a = self.b / 1.5

        self.matrtx = Matrix()
        self.matrtx[0, 0] = Startend("Начало", (self.a, self.b), self.font, (0, 1))
        down = self.generate_matrix((0, 0), (1, 0), self.code)
        self.matrtx[(down, 0)] = Startend("Конец", (self.a, self.b), self.font, (0, 1))


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

    def generate_matrix(self, last, vec, nexts):
        down = vec[0]
        for i in nexts:
            if type(i) is list:

                last = (last[0] + vec[0], last[1] + vec[1])
                down += vec[0]
                print(down)

                if "if" in i[0]:
                    self.matrtx[last] = If(i[0][i[0].index('(') + 1:i[0].index(')')], (self.a, self.b), self.font, last)
                elif "for" in i[0]:
                    self.matrtx[last] = For(i[0][i[0].index('(') + 1:i[0].index(')')], (self.a, self.b), self.font, last)
                elif "while" in i[0]:
                    self.matrtx[last] = If(i[0][i[0].index('(') + 1:i[0].index(')')], (self.a, self.b), self.font, last)
                elif "else" in i[0]:
                    self.matrtx[last] = Block(i[0], (self.a, self.b), self.font, last)
                else:
                    print(i[0][i[0].index('('):i[0].index(')')])

                addDown = self.generate_matrix(last, (1, 1), i[1:])
                last = (last[0] + addDown, last[1])
                down += addDown
            else:
                last = (last[0] + vec[0], last[1] + vec[1])
                down += vec[0]
                if "cout" in i:
                    self.matrtx[last] = Inout(i, (self.a, self.b), self.font, last)
                elif "cin" in i:
                    self.matrtx[last] = Inout(i, (self.a, self.b), self.font, last)
                else:
                    self.matrtx[last] = Block(i, (self.a, self.b), self.font, last)
        return down

    def render(self):
        cellHeight = self.a + self.w / 4  # TODO Подобрать значения
        cellWith = self.b + self.w / 4
        size = (int(self.matrtx.row * cellWith), int(self.matrtx.column * cellHeight))

        img = Image.new('RGB', size, 'white')
        img.save(self.name)
        img = Image.open(self.name)

        holst = ImageDraw.Draw(img)

        print(self.matrtx)
        for i in self.matrtx.keys():
            self.matrtx[i].draw((i[1] * cellWith + cellWith / 2, i[0] * cellHeight + cellHeight / 2), holst)

        img.save(self.name)
        img.show()