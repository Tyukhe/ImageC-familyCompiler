from PIL import Image, ImageDraw
from tree import Branch
from icc import slice_brackets
from pprint import pprint
from blocks import *
from textwrap import wrap


class WaysDrawer:
    def __init__(self, holst, sellSize):
        self.holst = holst
        self.image = holst.im
        self.cell = sellSize

    def is_line_poss(self, xy1, xy2, width=3):
        x1, y1 = int(xy1[0]), int(xy1[1])
        x2, y2 = int(xy2[0]), int(xy2[1])
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        x, y = x1, y1
        while True:
            pixel = self.image.getpixel((x, y))
            if pixel[0] == 0 and pixel[1] == 0 and pixel[2] == 0:
                if (x - x1)**2 + (y - y1)**2 > width**2 and (x - x2)**2 + (y - y2)**2 > width**2:
                    return x, y
            if x == x2 and y == y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy

        return False

    def draw_way(self, current, nexts):
        if len(nexts) == 0:
            return
        if current.x == nexts[0].x and current.y < nexts[0].y:
            current.draw_arrows(self.cell, self.holst, (0, 0, 0, 1))
            self.holst.line((current.get_points(self.cell)[7], nexts[0].get_points(self.cell)[4]), 'black',
                            current.lineWidth)
            nexts[0].draw_arrows(self.cell, self.holst, (1, 0, 0, 0))
        elif current.x == nexts[0].x and current.y > nexts[0].y:
            current.draw_arrows(self.cell, self.holst, (0, 0, 0, 1))
            self.holst.line((current.get_points(self.cell)[7], current.get_points(self.cell)[5][0],
                             current.get_points(self.cell)[7][1]),
                            'black', current.lineWidth)
            self.holst.line((current.get_points(self.cell)[5][0], current.get_points(self.cell)[7][1],
                             nexts[0].get_points(self.cell)[5]),
                            'black', current.lineWidth)
            nexts[0].draw_arrows(self.cell, self.holst, (0, 1, 0, 0))
        elif current.x > nexts[0].x:
            current.draw_arrows(self.cell, self.holst, (0, 0, 0, 1))
            print(self.is_line_poss(current.get_points(self.cell)[7], (current.get_points(self.cell)[7][0],
                             current.get_points(self.cell)[7][1] + current.lineWidth * 4)))
            self.holst.line((current.get_points(self.cell)[7], current.get_points(self.cell)[7][0],
                             current.get_points(self.cell)[7][1] + current.lineWidth * 4),
                            'black', current.lineWidth)
            print(self.is_line_poss((current.get_points(self.cell)[7][0],
                             current.get_points(self.cell)[7][1] + current.lineWidth * 4),
                                    (nexts[0].get_points(self.cell)[6][0],
                             current.get_points(self.cell)[7][1] + current.lineWidth * 4)))
            self.holst.line((current.get_points(self.cell)[7][0],
                             current.get_points(self.cell)[7][1] + current.lineWidth * 4,
                             nexts[0].get_points(self.cell)[6][0],
                             current.get_points(self.cell)[7][1] + current.lineWidth * 4),
                            'black', current.lineWidth)
            print(self.is_line_poss((nexts[0].get_points(self.cell)[6][0],
                             current.get_points(self.cell)[7][1] + current.lineWidth * 4),
                                    (nexts[0].get_points(self.cell)[6][0], nexts[0].get_points(self.cell)[4][1])))
            self.holst.line((nexts[0].get_points(self.cell)[6][0],
                             current.get_points(self.cell)[7][1] + current.lineWidth * 4,
                             nexts[0].get_points(self.cell)[6][0], nexts[0].get_points(self.cell)[4][1]),
                            'black', current.lineWidth)
            self.holst.line((nexts[0].get_points(self.cell)[6][0], nexts[0].get_points(self.cell)[4][1],
                             nexts[0].get_points(self.cell)[4]),
                            'black', current.lineWidth)
            nexts[0].draw_arrows(self.cell, self.holst, (1, 0, 0, 0))
        else:
            current.draw_arrows(self.cell, self.holst, (0, 0, 0, 1))
            self.holst.line((current.get_points(self.cell)[7], current.get_points(self.cell)[7][0],
                             nexts[0].get_points(self.cell)[4][1]),
                            'black', current.lineWidth)
            self.holst.line(
                (current.get_points(self.cell)[7][0], nexts[0].get_points(self.cell)[4][1],
                 nexts[0].get_points(self.cell)[4]),
                'black', current.lineWidth)
            nexts[0].draw_arrows(self.cell, self.holst, (1, 0, 0, 0))
        if len(nexts) > 1:
            if current.x < nexts[1].x and current.y < nexts[1].y:
                current.draw_arrows(self.cell, self.holst, (0, 0, 1, 0))
                self.holst.line((current.get_points(self.cell)[6], nexts[1].get_points(self.cell)[4][0],
                                 current.get_points(self.cell)[6][1]),
                                'black', current.lineWidth)
                self.holst.line(
                    (nexts[1].get_points(self.cell)[4][0], current.get_points(self.cell)[6][1],
                     nexts[1].get_points(self.cell)[4]),
                    'black', current.lineWidth)
                nexts[1].draw_arrows(self.cell, self.holst, (1, 0, 0, 0))
            else:
                current.draw_arrows(self.cell, self.holst, (0, 0, 1, 0))
                self.holst.line((current.get_points(self.cell)[6], current.get_points(self.cell)[6][0],
                                 nexts[1].get_points(self.cell)[4][1]),
                                'black', current.lineWidth)
                self.holst.line(
                    (current.get_points(self.cell)[6][0], nexts[1].get_points(self.cell)[4][1],
                     nexts[1].get_points(self.cell)[4]),
                    'black', current.lineWidth)
                nexts[1].draw_arrows(self.cell, self.holst, (1, 0, 0, 0))
            # self.holst.line((current.x * self.cell[0] + self.cell[0] / 2, current.y * self.cell[1] + self.cell[1] / 2,
            # nexts[1].item.x * self.cell[0] + self.cell[0] / 2,
            # nexts[1].item.y * self.cell[1] + self.cell[1] / 2), 'black', current.line)


class Scheme:
    def __init__(self, name, tree, font, glob=None):
        self.types = ["short", "int", "long", "float", "double", "char", "unsigned short", "unsigned int", "unsigned long", "unsigned float", "unsigned double"]
        self.counter = 0

        self.name = f'{name}.png'
        self.font = font
        self.tree = Branch(Startend("Начало", font), self.make_tree(tree, font))
        self.tree.item.set_global_name(name)
        self.matrix, _ = self.tree.get_matrix((0, 0))

        maxString = ""
        for i in self.tree:
            if len(i.item.get_max_str()) > len(maxString):
                maxString = i.item.get_max_str()
        self.w, self.h = self.font.getmask(maxString).getbbox()[2], self.font.getmask(maxString).getbbox()[3]
        self.b = self.w * 1# .4  # TODO подобрать значение
        self.a = self.b / 1.5

        for key in self.matrix.keys():
            self.matrix[key].prepare(key, (self.a, self.b), int(font.size * 0.19))

    def make_block(self, text, font):
        if any([j in text and text.index(j) == 0 for j in self.types]):
            if '=' in text:
                res = ""
                while "=" in text:
                    i = j = text.index("=")
                    while i - 1 > 0 and text[i - 1] != ',':
                        i -= 1
                    while j + 1 < len(text) and text[j + 1] != ',':
                        j += 1
                    res += text[i + 1:j + 1] + ', '
                    text = text[text.index("=") + 1:]
                return Block(res[:-2], font)
            else:
                return False
        elif 'cin' in text:
            text = text.replace(" >> ", "").replace('endl', "").replace("cin", '')
            return Inout(['Ввод'] + wrap(text, 200), font)
        elif 'cout' in text:
            text = text.replace(" << ", "").replace('endl', "").replace("cout", '')
            return Inout(['Вывод'] + wrap(text, 200), font)
        elif 'if' in text:
            return If(text[text.index('(') + 1:slice_brackets(text, text.index('('))], font)
        elif 'for' in text:
            return For(text[text.index('(') + 1:slice_brackets(text, text.index('('))], font)
        elif 'whilend' in text:
            return While(f'Цикл №{text[text.index('Е') + 1:text.index('З')]}', font, False)
        elif 'while' in text:
            return While([f'Цикл №{text[text.index('Е') + 1:text.index('З')]}',
                          text[text.index('(') + 1:slice_brackets(text, text.index('('))]], font, True)
        elif "return" in text:
            return Startend("Конец", font)  # Inout(["Вывод", text[7:]], font)
        elif '(' in text and text[text.index('(') - 1] not in ['+', '-', '*', '/', ' ']:
            return Func(text, font)
        return Block(text, font)

    def make_tree(self, nodes, font, elss=0, count=None):
        tree = []
        for node in nodes:
            if isinstance(node, list):
                if 'if' in node[0]:
                    f = lambda x: [f(i) if isinstance(i, list) else i.set_els(elss) for i in x]
                    tree.append(f(self.make_tree(node, font, elss + 1)))
                elif 'else' in node[0]:
                    f = lambda x: [f(i) if isinstance(i, list) else i.set_els(elss) for i in x]
                    tree += f(self.make_tree(node[1:], font))
                    elss += 1
                elif 'for' in node[0]:
                    tree.append(self.make_tree(node, font))
                elif 'while' in node[0]:
                    if count is None:
                        tree.append(
                            self.make_tree([node[0] + f'Е{self.counter}З'] + node[1:] + [f'whilendЕ{self.counter}З'], font, 0, self.counter))
                        self.counter += 1
                    else:
                        count += 1
                        tree.append(
                            self.make_tree([node[0] + f'Е{count}З'] + node[1:] + [f'whilendЕ{count}З'],
                                           font, 0, count))
                        self.counter += count
                else:
                    tree += self.make_tree(node, font)
            else:
                blocks = self.make_block(node, font)
                if blocks:
                    if isinstance(blocks, list):
                        tree += blocks
                    else:
                        tree.append(blocks)
        return tree

    def render(self):
        cellHeight = self.a + self.w / 4  # TODO Подобрать значения
        cellWith = self.b + self.w / 4
        size = (int(self.matrix.column * cellWith), int(self.matrix.row * cellHeight))
        print(size)

        img = Image.new('RGB', size, 'white')
        img.save(self.name)
        img = Image.open(self.name)

        holst = ImageDraw.Draw(img)
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        letter = 0

        for key in self.matrix.keys():
            self.matrix[key].draw((cellWith, cellHeight), holst)
        drawer = WaysDrawer(holst, (cellWith, cellHeight))
        for i in self.tree:
            # i.item.draw_ways((cellWith, cellHeight), holst, [j.item for j in i.get_children()])
            drawer.draw_way(i.item, [j.item for j in i.get_children()])
        img.save(self.name)
        img.show()
