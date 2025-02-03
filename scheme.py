from PIL import Image, ImageDraw
from tree import Branch
from icc import slice_brackets
from pprint import pprint
from blocks import *


class Scheme:
    def __init__(self, name, tree, font, glob=None):
        self.types = ["int", "long", "float", "char"]

        self.name = f'{name}.png'
        self.font = font
        self.tree = Branch(Startend("Начало", font), self.make_tree(tree, font))
        self.tree.item.set_global_name(name)
        self.matrix, _ = self.tree.get_matrix((0, 0))

        maxString = ""
        for i in self.tree:
            if len(i.get_max_str()) > len(maxString):
                maxString = i.get_max_str()
        self.w, self.h = self.font.getmask(maxString).getbbox()[2], self.font.getmask(maxString).getbbox()[3]
        self.b = self.w * 1.3 # TODO подобрать значение
        self.a = self.b / 1.5

        for key in self.matrix.keys():
            self.matrix[key].prepare(key, (self.a, self.b))

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
            return Inout(['Ввод', text.replace(" >> ", "").replace('endl', "").replace("cin", '')], font)
        elif 'cout' in text:
            return Inout(['Вывод', text.replace(" << ", "").replace('endl', "").replace("cout", '')], font)
        elif 'if' in text:
            return If(text[text.index('(') + 1:slice_brackets(text, text.index('('))], font)
        elif 'for' in text:
            return For(text[text.index('(') + 1:slice_brackets(text, text.index('('))], font)
        elif 'while' in text:
            return While(text[text.index('(') + 1:slice_brackets(text, text.index('('))], font)
        elif "return" in text:
            return [Inout(["Вывод", text[7:]], font), Startend("Конец", font)]
        return Block(text, font)


    def make_tree(self, nodes, font, elss=0):
        tree = []
        for node in nodes:
            if isinstance(node, list):
                if 'if' in node[0]:
                    f = lambda x: [f(i) if isinstance(i, list) else i.set_els(elss) for i in x]
                    tree.append(f(self.make_tree(node, font, elss + 1)))
                elif 'else' in node[0]:
                    tree += list(map(lambda x: x.set_els(elss), self.make_tree(node[1:], font)))
                    elss += 1
                elif any(i in node[0] for i in ['for', 'while']):
                    tree.append(self.make_tree(node, font))
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

        for key in self.matrix.keys():
            self.matrix[key].draw((cellWith, cellHeight), holst)
        for i in self.tree:
            i.item.draw_ways((cellWith, cellHeight), holst, [i.item for i in i.get_children()])
        img.save(self.name)
        img.show()
