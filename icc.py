from PIL import Image, ImageDraw, ImageFont
from pprint import pprint
from sys import argv

class Scheme:
    def __init__(self, size=(200, 200), fontSize=16):
        self.img = Image.new('RGB', size, 'white')
        self.img.save('a.png')
        self.img = Image.open('a.png')

        self.font = ImageFont.truetype(r'Times_New_Roman.ttf', fontSize)

        self.holst = ImageDraw.Draw(self.img)

    def draw_block(self, xy, text):
        x, y = xy[0], xy[1]
        w, h = self.font.getmask(text).getbbox()[2], self.font.getmask(text).getbbox()[3] + 3

        b = w * 1.2
        a = b / 2

        self.holst.text((x - w / 2, y - h / 2), text, fill='black', font=self.font)
        # self.holst.rectangle([(x - w / 2, y - h / 2 + 3), (x + w / 2, y + h / 2)], outline="black") # TODO

        self.holst.rectangle((x - b / 2, y - a / 2, x + b / 2, y + a / 2), outline ="black", width=2)

        self.img.save('a.png')

    def draw_if(self, xy, text):
        x, y = xy[0], xy[1]
        w, h = self.font.getmask(text).getbbox()[2], self.font.getmask(text).getbbox()[3] + 3

        b = w * 1.2
        a = b / 1.5

        self.holst.text((x - w / 2, y - h / 2), text, fill='black', font=self.font)
        self.holst.line((x + b / 2, y, x, y - a / 2), 'black', 2)
        self.holst.line((x, y - a / 2, x - b / 2, y), 'black', 2)
        self.holst.line((x - b / 2, y, x, y + a / 2), 'black', 2)
        self.holst.line((x, y + a / 2, x + b / 2, y), 'black', 2)

        self.img.save('a.png')

    def draw_for(self, xy, text):
        x, y = xy[0], xy[1]
        w, h = self.font.getmask(text).getbbox()[2], self.font.getmask(text).getbbox()[3] + 3

        b = w * 1.2
        a = b / 2

        self.holst.text((x - w / 2, y - h / 2), text, fill='black', font=self.font)
        self.holst.line((x + b / 2, y, x + a / 2, y - a / 2), 'black', 2)
        self.holst.line((x + a / 2, y - a / 2, x - a / 2, y - a / 2), 'black', 2)
        self.holst.line((x - a / 2, y - a / 2, x - b / 2, y), 'black', 2)
        self.holst.line((x - b / 2, y, x - a / 2, y + a / 2), 'black', 2)
        self.holst.line((x - a / 2, y + a / 2, x + a / 2, y + a / 2), 'black', 2)
        self.holst.line((x + a / 2, y + a / 2, x + b / 2, y), 'black', 2)

        self.img.save('a.png')

    def draw_func(self, xy, text):
        x, y = xy[0], xy[1]
        w, h = self.font.getmask(text).getbbox()[2], self.font.getmask(text).getbbox()[3] + 3

        b = w * 1.2 / 0.85
        a = b / 2

        self.holst.text((x - w / 2, y - h / 2), text, fill='black', font=self.font)

        self.holst.rectangle((x - b / 2, y - a / 2, x + b / 2, y + a / 2), outline ="black", width=2)
        self.holst.line((x + b / 2 - a * 0.15, y - a / 2, x + b / 2 - a * 0.15, y + a / 2), 'black', 2)
        self.holst.line((x - b / 2 + a * 0.15, y - a / 2, x - b / 2 + a * 0.15, y + a / 2), 'black', 2)

        self.img.save('a.png')

    def draw_inout(self, xy, text):
        x, y = xy[0], xy[1]
        w, h = self.font.getmask(text).getbbox()[2], self.font.getmask(text).getbbox()[3] + 3

        b = w * 2.4 / 1.75
        a = b / 1.5

        self.holst.text((x - w / 2, y - h / 2), text, fill='black', font=self.font)

        self.holst.line((x + b / 2 - a * 0.25, y + a / 2, x + b / 2, y - a / 2), 'black', 2)
        self.holst.line((x + b / 2, y - a / 2, x - b / 2 + a * 0.25, y - a / 2), 'black', 2)
        self.holst.line((x - b / 2 + a * 0.25, y - a / 2, x - b / 2, y + a / 2), 'black', 2)
        self.holst.line((x - b / 2, y + a / 2, x + b / 2 - a * 0.25, y + a / 2), 'black', 2)

        self.img.save('a.png')



def a():

    font = ImageFont.truetype(r'Times_New_Roman.ttf', 14)
    idrw = ImageDraw.Draw(scheme)

    text = '13ЫВЫСФЫС()вссывсывсжвсы;;;ывывс'

    x, y = 25, 25

    idrw.text((x, y), text, fill='black', font=font)

    w = font.getmask(text).getbbox()[2]
    h = font.getmask(text).getbbox()[3]
    y += 3

    idrw.line((x, y, x + w, y), 'black', 1)
    idrw.line((x, y, x, y + h), 'black', 1)
    idrw.line((x + w, y, x + w, y + h), 'black', 1)
    idrw.line((x, y + h, x + w, y + h), 'black', 1)

    scheme.save('a.png')
    scheme = Image.open('a.png')

    scheme.show()

def make_tree(code):
    nodes = []
    node = ''
    i = 0
    c = False
    while i < len(code):
        if c:
            if code[i] == '}':
                nodes.append(make_tree(code[c + 1:i]))
                c = False
        else:
            if code[i] == ';':
                nodes.append(node)
                node = ''
            elif code[i] == '{':
                nodes.append(node)
                node = ''
                c = i
            else:
                node += code[i]
        i += 1
    return nodes

if __name__ == "__main__":
    # ----------
    #if len(argv) == 1:
        #print("No file")
        #exit(1)

    #file = open(argv[1], 'r')
    # ----------
    # file = open('main.cpp', 'r')
    # ----------
    # code = ['' if l[0] == '#' else l.replace('\n', '').replace('    ', '') for l in file.readlines()]
    # file.close()

    # funcs = {}
    # code = ''.join(code)
    # nodes = make_tree(code)

    # pprint(code)
    # pprint(nodes)
    s = Scheme((1280, 920), 14)
    s.draw_inout((250, 250), "Hello sascascadasdasdasdscasddf")
    s.img.show()
