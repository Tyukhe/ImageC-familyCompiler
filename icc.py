from matrix import Matrix
from PIL import Image, ImageDraw, ImageFont
from scheme import *
from blocks import *
from tree import *
from sys import argv
from pprint import pprint


brackets = {
    '(':')',
    '{':'}',
    '[':']',
    '<':'>',
}


def slice_brackets(text, index):
    elementary = text[index]
    finite = brackets[elementary]
    count = 0
    for i, s in enumerate(text[index:]):
        if s == elementary:
            count += 1
        elif s == finite:
            count -= 1
        if count == 0:
            return index + i
    return 0


def make_nodes(code):
    nodes = []
    node = ''
    i = 0
    while i < len(code):
        if code[i] == ';':
            nodes.append(node)
            node = ''
        elif code[i] == '{':
            end = slice_brackets(code, i)
            nodes.append([node] + make_nodes(code[i + 1:end]))
            node = ''
            i = end
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
    code = ''.join(['' if l[0] == '#' else l.replace('\n', '') \
        .replace('    ', '') for l in file.readlines()])
    file.close()

    font = ImageFont.truetype(r'font.ttf', 20) # TODO подобрать значение

    nodes = make_nodes(code)

    parts = {0: []}
    funcs = []

    for i in nodes:
        if type(i) is list:
            parts[i[0]] = i[1:]
            funcs.append(i[0])
        else:
            parts[0].append(i)

    schemes = {}

    for func in funcs:
        schemes[func] = Scheme(func, parts[func], font, parts[0])

    for func in funcs:
        schemes[func].render()
