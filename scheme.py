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


class Scheme:
    def __init__(self, name, code, font, glob=None):
        self.types = ["int", "long", "float", "char"]

        self.name = f'{name}.png'
        self.font = font

        self.maxString = self.get_max(code)
        self.w, self.h = self.font.getmask(self.maxString).getbbox()[2], self.font.getmask(self.maxString).getbbox()[3]
        self.b = self.w * 1.25 # TODO подобрать значение
        self.a = self.b / 1.5

        self.matrtx = Matrix()
        self.blocks = self.generate_list(code)
        print(code)
        print(self.blocks)


    def make_block(self, text):
        if "cout" in text:
            return Inout(text.replace(" << ", "").replace('"', "").replace('endl', "").replace("cout", 'Вывод "') + '"', (self.a, self.b), self.font)
        elif "cin" in text:
            return Inout(text.replace(" >> ", "").replace('"', "").replace('endl', "").replace("cin", 'Ввод '), (self.a, self.b), self.font)
        elif any([j in text and text.index(j) == 0 for j in self.types]) and "=" in text:
            res = ""
            buffer = ""
            for j in text:
                if j == ',':
                    if '=' in buffer:
                        res += buffer + ", "
                    else:
                        buffer = ""
                else:
                    buffer += j
            if '=' in buffer:
                res += buffer[1:] + ", "
            if res == "":
                return None
            else:
                res = res[:-2]
            return res
        else:
            return Block(text, (self.a, self.b), self.font)

    def generate_list(self, code):
        res = []
        for i in code:
            if type(i) == list:
                res.append(self.generate_list(i))
            else:
                res.append(self.make_block(i))
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
        size = (int(self.matrtx.row * cellWith), int(self.matrtx.column * cellHeight))

        img = Image.new('RGB', size, 'white')
        img.save(self.name)
        img = Image.open(self.name)

        holst = ImageDraw.Draw(img)

        # print(self.matrtx)
        for i in self.matrtx.keys():
            self.matrtx[i].draw((i[1] * cellWith + cellWith / 2, i[0] * cellHeight + cellHeight / 2), holst)
            # self.matrtx[i].draw_arrows((i[1] * cellWith + cellWith / 2, i[0] * cellHeight + cellHeight / 2), (cellWith, cellHeight), holst, (True, True, True, True))

        img.save(self.name)
        img.show()