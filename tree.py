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
        res = [str(self.item)]
        for i in self.value:
            res.append(str(i))
        return str(res)

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

    def get_list(self):
        res = [self]
        for i in self.value:
            res += i.get_list()
        return res

    def get_next(self):
        if len(self.parent.value) == self.addr[-1] + 1:
            return self.parent.next()
        return self.parent.value[self.addr[-1] + 1]

    def get_previous(self):
        if self.addr[-1] == 0:
            return self.parent
        return self.parent.value[self.addr[-1] - 1]

    def get_matrix(self, xy):
        res = Matrix()
        x, y = xy
        if type(self.item) == While:
            x += 1
        res[x, y] = self.item
        if type(self.item) == If:
            x += 1
        down = 1
        for i in self.value:
            lcount = 0
            ldown = 0
            lmatrix, ldown = i.get_matrix((x, y + lcount + down))
            while not(res & lmatrix):
                lcount += 1
                lmatrix, ldown = i.get_matrix((x, y + lcount + down))
            down += ldown
            res += lmatrix
        return res, down

# b = Branch('r', ['0', '1', '2', ['3', '30', '31'], ['4', ['40', '400'], ['41', '410', '411']], ['5', '50', ['51', '510']], '6'])
# pprint(b.get_matrix((0, 0)))
