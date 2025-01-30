class Matrix:
    def __init__(self):
        self.matrix = [[None]]
        self.row = 1
        self.column = 1

    def __len__(self):
        return self.row * self.column

    def get_size(self):
        fc = self.column
        fr = self.row
        lc = 0
        lr = 0
        for i in range(self.column):
            if any(self.matrix[i]):
                if fc > i:
                    fc = i
                if lc < i:
                    lc = i
            for j in range(self.row):
                if self.matrix[i][j]:
                    if fr > j:
                        fr = j
                    if lr < j:
                        lr = j
        return lc - fc + 1, lr - fr + 1

    def __getitem__(self, key):
        if type(key) != tuple or key[0] < 0 or key[1] < 0:
            raise TypeError
        try:
            return self.matrix[key[0]][key[1]]
        except IndexError:
            return None

    def __setitem__(self, key, value):
        if type(key) != tuple or key[0] < 0 or key[1] < 0:
            raise TypeError
        while key[0] >= self.column:
            self.matrix.append([None] * self.row)
            self.column += 1
        while key[1] >= self.row:
            for i in range(self.column):
                self.matrix[i].append(None)
            self.row += 1
        self.matrix[key[0]][key[1]] = value


    def __delitem__(self, key):
        if type(key) != tuple or key[0] < 0 or key[1] < 0:
            raise TypeError
        try:
            self.matrix[key[0]][key[1]] = None
        except IndexError:
            pass

    def __iter__(self):
        res = []
        for i in self.matrix:
            for j in i:
                if j is not None:
                    res.append(j)
        return res.__iter__()

    def keys(self):
        res = []
        for i in range(self.column):
            for j in range(self.row):
                if self.matrix[i][j] is not None:
                    res.append((i, j))
        return res

    def __str__(self):
        res = ""
        for i in range(self.row):
            for j in range(self.column):
                if self.matrix[j][i] is None:
                    res += f"~\t\t"
                else:
                    res += f"{self.matrix[j][i]}\t\t"
            res += "\n"
        return res

    def __repr__(self):
        res = ""
        for i in range(self.row):
            for j in range(self.column):
                if self.matrix[j][i] is None:
                    res += f"~\t\t"
                else:
                    res += f"{self.matrix[j][i]}\t\t"
            res += "\n"
        return res

    def __and__(self, other):
        if len(set(self.keys()) & set(other.keys())) == 0:
            return True
        return False

    def __iadd__(self, other):
        for i in other.keys():
            self[i] = other[i]
        return self
