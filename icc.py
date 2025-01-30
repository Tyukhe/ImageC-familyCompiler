from pycparser.c_ast import While

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


def make_block(text, font):
    if 'if' in text:
        return If(text[text.index('(') + 1:slice_brackets(text, text.index('('))], font)
    elif 'for' in text:
        return For(text[text.index('(') + 1:slice_brackets(text, text.index('('))], font)
    elif 'while' in text:
        return While(text[text.index('(') + 1:slice_brackets(text, text.index('('))], font)
    else:
        return Block(text, font)


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


def make_tree(nodes, font):
    tree = []
    for node in nodes:
        if isinstance(node, list):
            if any(i in node[0] for i in ['if', 'for', 'while']):
                tree.append(make_tree(node, font))
            elif 'else' in node[0]:
                tree += make_tree(node[1:], font)
            else:
                tree += make_tree(node, font)
        else:
            tree.append(make_block(node, font))
    return tree


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

    font = ImageFont.truetype(r'font.ttf', 14) # TODO подобрать значение

    nodes = make_nodes(code)

    parts = {0: []}
    funcs = []

    for i in nodes:
        if type(i) is list:
            parts[i[0]] = Branch(Startend("Начало", font), make_tree(i[1:], font))
            funcs.append(i[0])
        else:
            parts[0].append(make_block(i, font))

    schemes = {}

    for func in funcs:
        schemes[func] = Scheme(func, parts[func], font, parts[0])

    for func in funcs:
        schemes[func].render()
