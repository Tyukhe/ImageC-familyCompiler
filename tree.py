from matrix import Matrix
from pprint import pprint
from blocks import *

class Branch:
    def __init__(self, item=None, value=None, parent=None):
        if item is None:
            self.item = 'root'
        else:
            self.item = item
        if value is None:
            self.value = list()
        else:
            self.value = [Branch(node[0], node[1:], self) if isinstance(node, list) else Branch(node, None, self) for node in value]
        self.parent = parent
        self.addr = []
        if self.parent is None:
            self.addressing()

    def __str__(self):
        return str(self.get_tree())

    def __repr__(self):
        return str(self.item)

    def __getitem__(self, addr):
        if type(addr) is tuple:
            if len(addr) == 1:
                return self.value[addr[0]]
            return self.value[addr[0]][tuple(addr[1:])]
        return self.value[addr]

    def __iter__(self):
        return iter(self.get_list())

    def __len__(self):
        return len(self.value)

    def addressing(self):
        for i in self:
            i.set_addr()

    def set_addr(self):
        if self.parent is None:
            self.addr = list()
        else:
            self.addr = self.parent.addr + [self.parent.value.index(self)]

    def get_root(self):
        if self.parent is None:
            return self
        return self.parent.get_root()

    def get_tree(self):
        res = [self]
        for i in self.value:
            res.append(i.get_tree())
        return res

    def get_list(self):
        res = [self]
        for i in self.value:
            res += i.get_list()
        return res

    def get_next(self):
        if self.parent is None or (type(self.item) == Startend and self.item.text[0] != "Начало"):
            return None
        if len(self.parent.value) != self.addr[-1] + 1:
            return self.parent.value[self.addr[-1] + 1]
        if type(self.parent.item) == For:
            return self.parent
        if type(self.parent.item) == While:
            return self.parent.get_next()
        res = self.parent.get_next()
        if res is None:
            return None
        while res.item.elss == self.parent.item.elss:
            res = res.get_next()
            if res is None:
                return None
        return res

    def get_children(self):
        if not (self.parent is None) and self.parent.parent is None and len(self.parent.value) == self.addr[-1] + 1:
            return []
        res = [] if self.get_next() is None else [self.get_next()]
        if len(self.value) != 0:
            res.append(self.value[0])
        if type(self.item) == For:
            res = res[::-1]
        if type(self.item) == While and self.item.start:
            res = [res[-1]]
        return res

    def get_matrix(self, xy):
        res = Matrix()
        x, y = xy
        if type(self.item) == While and self.item.start and type(self.parent.item) == While:
            x += 1
        res[x, y] = self.item
        if type(self.item) == If:
            x += 1
        down = 1
        for i in self.value:
            lcount = 0
            lmatrix, ldown = i.get_matrix((x, y + lcount + down))
            while not(res & lmatrix):
                lcount += 1
                lmatrix, ldown = i.get_matrix((x, y + lcount + down))
            down += ldown
            res += lmatrix
        return res, down

# b = Branch('r', ['0', '1', '2', ['3', '30', '31'], ['4', ['40', '400'], ['41', '410', '411']], ['5', '50', ['51', '510']], '6'])
# pprint(b.get_matrix((0, 0)))
