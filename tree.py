from matrix import Matrix
from pprint import pprint

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
        return str(self.item)

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

    def get_layers(self):
        res = [[self]]
        counter = [[self, -1]]
        while len(counter) != 0:
            local_res = []
            new_counter = []
            for i in counter:
                i[1] += 1
                if len(i[0].value) != i[1]:
                    new_counter.append(i)
                    local_res.append(i[0][i[1]])
                    if len(i[0][i[1]].value) != 0:
                        new_counter.append([i[0][i[1]], -1])
            res.append(local_res)
            counter = new_counter
        del res[-1]
        return res

    def get_matrix(self, xy, root=True):
        res = Matrix()
        res[xy] = self
        x, y = xy
        if not root:
            x += 1
        c = 1
        for i in range(len(self.value)):
            if len(self.value[i]) == 0:
                res[x, y + i + c] = self.value[i]
            else:
                for j in range(10):
                    print('Warning')
                    matrix = self.value[i].get_matrix((x + j, y + i + c), False)
                    if matrix & res:
                        res += matrix
                        # c += matrix.column
                        break
                else:
                    raise MemoryError
        return res

b = Branch('r', ['0', '1', '2', ['3', '30', '31'], ['4', ['40', '400'], ['41', '410', '411']], ['5', '50', ['51', '510']], '6'])
pprint(b.get_matrix((0, 0)))
