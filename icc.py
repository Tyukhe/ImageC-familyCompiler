from matrix import Matrix
from PIL import Image, ImageDraw, ImageFont
from scheme import *
from sys import argv


def make_tree(code):
    nodes = []
    node = ''
    i = 0
    c = False
    count = 0
    while i < len(code):
        if c:
            if code[i] == '{':
                count += 1
            elif code[i] == '}':
                count -= 1
                if count == 0:
                    if 'else' in node:
                        nodes[-1].append([node] + make_tree(code[c + 1:i]))
                        node = ''
                        c = False
                    else:
                        nodes.append([node] + make_tree(code[c + 1:i]))
                        node = ''
                        c = False
        else:
            if code[i] == ';':
                if 'for' not in node:
                    nodes.append(node)
                    node = ''
                else:
                    node += code[i]
            elif code[i] == '{':
                c = i
                count = 1
            else:
                node += code[i]
        i += 1
    return nodes


if __name__ == "__main__":
    # ----------
    # if len(argv) == 1:
    # print("No file")
    # exit(1)

    # file = open(argv[1], 'r')
    # ----------
    file = open('main.cpp', 'r')
    # ----------
    code = ['' if l[0] == '#' else l.replace('\n', '') \
        .replace('    ', '') \
        .replace('<<', '') \
        .replace('>>', '') \
        .replace('endl', '') for l in file.readlines()]
    file.close()

    code = ''.join(code)
    nodes = make_tree(code)
    parts = {0: []}
    funcs = []

    for i in nodes:
        if type(i) is list:
            parts[i[0]] = i[1:]
            funcs.append(i[0])
        else:
            parts[0].append(i)

    schemes = {}

    font = ImageFont.truetype(r'font.ttf', 18) # TODO подобрать значение

    for func in funcs:
        schemes[func] = Scheme(func, parts[func], font, parts[0])

    for func in funcs:
        schemes[func].render()
