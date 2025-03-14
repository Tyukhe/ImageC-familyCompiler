class Block:
    def __init__(self, text, font):
        if isinstance(text, list):
            self.text = text
        else:
            self.text = [text]
        self.font = font

        self.h = self.font.getmask(self.text[0]).getbbox()[3] * 0.75

        self.a = -1
        self.b = -1
        self.x = -1
        self.y = -1
        self.lineWidth = -1
        self.elss = set()

    def __str__(self):
        return " ".join(self.text)

    def __repr__(self):
        return str(type(self)) + ':' + str(self)

    def get_max_str(self):
        res = ""
        if not isinstance(self.text, list):
            return self.text
        for i in self.text:
            if len(res) < len(i):
                res = i
        return res

    def set_els(self, els):
        self.elss.add(els)
        return self

    def prepare(self, xy, ab, lineWidth):
        self.x, self.y = xy
        self.a, self.b = ab
        self.lineWidth = lineWidth

    def get_points(self, cell):
        x, y = self.x * cell[0] + cell[0] / 2, self.y * cell[1] + cell[1] / 2
        return (x, y - self.a / 2), (x - self.b / 2, y), (x + self.b / 2, y), (x, y + self.a / 2), (
        x, y - self.a / 2 - (cell[1] - self.a) * 0.5 + self.lineWidth * 2), (
        x - self.b / 2 - (cell[0] - self.b) * 0.5 + self.lineWidth * 2, y), (
        x + self.b / 2 + (cell[0] - self.b) * 0.5 - self.lineWidth * 2, y), (
        x, y + self.a / 2 + (cell[1] - self.a) * 0.5 - self.lineWidth * 2)

    def draw_arrows(self, cell, holst, dirs=(True, False, False, True)):
        x, y = self.x * cell[0] + cell[0] / 2, self.y * cell[1] + cell[1] / 2
        cx, cy = cell
        if dirs[0]:
            holst.line((self.get_points(cell)[0], self.get_points(cell)[4]), 'black', self.lineWidth)
            holst.line((self.get_points(cell)[0], self.get_points(cell)[0][0] + self.a / 60,
                        self.get_points(cell)[0][1] - self.a / 25), 'black', self.lineWidth)
            holst.line((self.get_points(cell)[0], self.get_points(cell)[0][0] - self.a / 60,
                        self.get_points(cell)[0][1] - self.a / 25), 'black', self.lineWidth)
        if dirs[1]:
            holst.line((self.get_points(cell)[1], self.get_points(cell)[5]), 'black', self.lineWidth)
            holst.line((self.get_points(cell)[1], self.get_points(cell)[1][0] - self.a / 25,
                        self.get_points(cell)[1][1] + self.a / 60), 'black', self.lineWidth)
            holst.line((self.get_points(cell)[1], self.get_points(cell)[1][0] - self.a / 25,
                        self.get_points(cell)[1][1] - self.a / 60), 'black', self.lineWidth)
        if dirs[2]:
            holst.line((self.get_points(cell)[2], self.get_points(cell)[6]), 'black', self.lineWidth)
        if dirs[3]:
            holst.line((self.get_points(cell)[3], self.get_points(cell)[7]), 'black', self.lineWidth)

    def draw(self, cell, holst):
        x, y = self.x * cell[0] + cell[0] / 2, self.y * cell[1] + cell[1] / 2
        l = len(self.text)
        for i, k in enumerate(self.text):
            holst.text((x, y + (self.h * ((i - (l - 1) / 2) * 2))), k, fill='black', font=self.font, anchor="mm")
        holst.rectangle((x - self.b / 2, y - self.a / 2, x + self.b / 2, y + self.a / 2), outline="black",
                        width=self.lineWidth)

        # holst.rectangle((x - cell[0] / 2, y - cell[1] / 2, x + cell[0] / 2, y + cell[1] / 2), outline="black", width=self.lineWidth)


class Startend(Block):
    def __init__(self, text, font):
        super().__init__(text, font)
        self.name = None

    def get_points(self, cell):
        x, y = self.x * cell[0] + cell[0] / 2, self.y * cell[1] + cell[1] / 2
        return (x, y - self.a / 4), (x - self.b / 2, y), (x + self.b / 2, y), (x, y + self.a / 4), (
        x, y - self.a / 4 - (cell[1] - self.a) * 0.5 + self.lineWidth * 2), (
        x - self.b / 2 - (cell[0] - self.b) * 0.5 + self.lineWidth * 2, y), (
        x + self.b / 2 + (cell[0] - self.b) * 0.5 - self.lineWidth * 2, y), (
        x, y + self.a / 4 + (cell[1] - self.a) * 0.5 - self.lineWidth * 2)

    def set_global_name(self, name):
        self.name = name

    def draw(self, cell, holst):
        x, y = self.x * cell[0] + cell[0] / 2, self.y * cell[1] + cell[1] / 2
        l = len(self.text)
        if not self.name is None:
            h = self.font.getmask(self.name).getbbox()[3] * 0.75
            holst.text((x, y - self.a / 4 - h), self.name, fill='black', font=self.font, anchor="mm")
        for i, k in enumerate(self.text):
            holst.text((x, y + (self.h * ((i - (l - 1) / 2) * 2))), k, fill='black', font=self.font, anchor="mm")
        holst.line((x + self.b / 2 - self.a / 4, y + self.a / 4, x - self.b / 2 + self.a / 4, y + self.a / 4), 'black',
                   self.lineWidth)
        holst.line((x + self.b / 2 - self.a / 4, y - self.a / 4, x - self.b / 2 + self.a / 4, y - self.a / 4), 'black',
                   self.lineWidth)
        holst.arc((x + self.b / 2 - self.a / 2, y - self.a / 4, x + self.b / 2, y + self.a / 4), -90, 90, 'black',
                  self.lineWidth)
        holst.arc((x - self.b / 2, y - self.a / 4, x - self.b / 2 + self.a / 2, y + self.a / 4), 90, -90, 'black',
                  self.lineWidth)

        # holst.rectangle((x - cell[0] / 2, y - cell[1] / 2, x + cell[0] / 2, y + cell[1] / 2), outline="black", width=self.lineWidth)


class If(Block):
    def draw(self, cell, holst):
        x, y = self.x * cell[0] + cell[0] / 2, self.y * cell[1] + cell[1] / 2
        l = len(self.text)
        for i, k in enumerate(self.text):
            holst.text((x, y + (self.h * ((i - (l - 1) / 2) * 2))), k, fill='black', font=self.font, anchor="mm")
        holst.line((x + self.b / 2, y, x, y - self.a / 2), 'black', self.lineWidth)
        holst.line((x, y - self.a / 2, x - self.b / 2, y), 'black', self.lineWidth)
        holst.line((x - self.b / 2, y, x, y + self.a / 2), 'black', self.lineWidth)
        holst.line((x, y + self.a / 2, x + self.b / 2, y), 'black', self.lineWidth)

        h = self.font.getmask("ДаНет").getbbox()[3]
        holst.text((x + self.b / 1.9 + h * 0.5, y - h * 1.5), "Да", fill='black', font=self.font)
        holst.text((x + h * 0.5, y + self.a / 2), "Нет", fill='black', font=self.font)

        # holst.rectangle((x - cell[0] / 2, y - cell[1] / 2, x + cell[0] / 2, y + cell[1] / 2), outline="black", width=self.lineWidth)


class For(Block):
    def draw(self, cell, holst):
        x, y = self.x * cell[0] + cell[0] / 2, self.y * cell[1] + cell[1] / 2
        l = len(self.text)
        for i, k in enumerate(self.text):
            holst.text((x, y + (self.h * ((i - (l - 1) / 2) * 2))), k, fill='black', font=self.font, anchor="mm")
        holst.line((x + self.b / 2, y, x + self.a / 2, y - self.a / 2), 'black', self.lineWidth)
        holst.line((x + self.a / 2, y - self.a / 2, x - self.a / 2, y - self.a / 2), 'black', self.lineWidth)
        holst.line((x - self.a / 2, y - self.a / 2, x - self.b / 2, y), 'black', self.lineWidth)
        holst.line((x - self.b / 2, y, x - self.a / 2, y + self.a / 2), 'black', self.lineWidth)
        holst.line((x - self.a / 2, y + self.a / 2, x + self.a / 2, y + self.a / 2), 'black', self.lineWidth)
        holst.line((x + self.a / 2, y + self.a / 2, x + self.b / 2, y), 'black', self.lineWidth)

        # holst.rectangle((x - cell[0] / 2, y - cell[1] / 2, x + cell[0] / 2, y + cell[1] / 2), outline="black", width=self.lineWidth)


class While(Block):
    def __init__(self, text, font, start=True):
        super().__init__(text, font)
        self.start = start

    def draw(self, cell, holst):
        x, y = self.x * cell[0] + cell[0] / 2, self.y * cell[1] + cell[1] / 2
        l = len(self.text)
        for i, k in enumerate(self.text):
            holst.text((x, y + (self.h * ((i - (l - 1) / 2) * 2))), k, fill='black', font=self.font, anchor="mm")
        if self.start:
            holst.line((x + self.b / 2, y, x + self.a / 2, y - self.a / 2), 'black', self.lineWidth)
            holst.line((x + self.a / 2, y - self.a / 2, x - self.a / 2, y - self.a / 2), 'black', self.lineWidth)
            holst.line((x - self.a / 2, y - self.a / 2, x - self.b / 2, y), 'black', self.lineWidth)
            holst.line((x - self.b / 2, y, x - self.b / 2, y + self.a / 2), 'black', self.lineWidth)
            holst.line((x - self.b / 2, y + self.a / 2, x + self.b / 2, y + self.a / 2), 'black', self.lineWidth)
            holst.line((x + self.b / 2, y + self.a / 2, x + self.b / 2, y), 'black', self.lineWidth)
        else:
            holst.line((x + self.b / 2, y, x + self.b / 2, y - self.a / 2), 'black', self.lineWidth)
            holst.line((x + self.b / 2, y - self.a / 2, x - self.b / 2, y - self.a / 2), 'black', self.lineWidth)
            holst.line((x - self.b / 2, y - self.a / 2, x - self.b / 2, y), 'black', self.lineWidth)
            holst.line((x - self.b / 2, y, x - self.a / 2, y + self.a / 2), 'black', self.lineWidth)
            holst.line((x - self.a / 2, y + self.a / 2, x + self.a / 2, y + self.a / 2), 'black', self.lineWidth)
            holst.line((x + self.a / 2, y + self.a / 2, x + self.b / 2, y), 'black', self.lineWidth)

        # holst.rectangle((x - cell[0] / 2, y - cell[1] / 2, x + cell[0] / 2, y + cell[1] / 2), outline="black", width=self.lineWidth)


class Func(Block):
    def draw(self, cell, holst):
        x, y = self.x * cell[0] + cell[0] / 2, self.y * cell[1] + cell[1] / 2
        l = len(self.text)
        for i, k in enumerate(self.text):
            holst.text((x, y + (self.h * ((i - (l - 1) / 2) * 2))), k, fill='black', font=self.font, anchor="mm")
        holst.rectangle((x - self.b / 2, y - self.a / 2, x + self.b / 2, y + self.a / 2), outline="black",
                        width=self.lineWidth)
        holst.line((x + self.b / 2 - self.a * 0.15, y - self.a / 2, x + self.b / 2 - self.a * 0.15, y + self.a / 2),
                   'black', self.lineWidth)
        holst.line((x - self.b / 2 + self.a * 0.15, y - self.a / 2, x - self.b / 2 + self.a * 0.15, y + self.a / 2),
                   'black', self.lineWidth)

        # holst.rectangle((x - cell[0] / 2, y - cell[1] / 2, x + cell[0] / 2, y + cell[1] / 2), outline="black", width=self.lineWidth)


class Inout(Block):
    def draw(self, cell, holst):
        x, y = self.x * cell[0] + cell[0] / 2, self.y * cell[1] + cell[1] / 2
        l = len(self.text)
        for i, k in enumerate(self.text):
            holst.text((x, y + (self.h * ((i - (l - 1) / 2) * 2))), k, fill='black', font=self.font, anchor="mm")
        holst.line((x + self.b / 2 - self.a * 0.25, y + self.a / 2, x + self.b / 2, y - self.a / 2), 'black',
                   self.lineWidth)
        holst.line((x + self.b / 2, y - self.a / 2, x - self.b / 2 + self.a * 0.25, y - self.a / 2), 'black',
                   self.lineWidth)
        holst.line((x - self.b / 2 + self.a * 0.25, y - self.a / 2, x - self.b / 2, y + self.a / 2), 'black',
                   self.lineWidth)
        holst.line((x - self.b / 2, y + self.a / 2, x + self.b / 2 - self.a * 0.25, y + self.a / 2), 'black',
                   self.lineWidth)

        # holst.rectangle((x - cell[0] / 2, y - cell[1] / 2, x + cell[0] / 2, y + cell[1] / 2), outline="black", width=self.lineWidth)
