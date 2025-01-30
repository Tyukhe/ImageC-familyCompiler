class Node:
    def __init__(self, item, parent=None):
        self.item = item
        self.parent = parent
        self.parents = []
        self.major = None
        self.minor = None

    def __getitem__(self, key):
        if key:
            return self.major
        return self.minor

    def add(self, item, index=0):
        if index:
            self.major = Node(item, self)
        else:
            self.minor = Node(item, self)

    def __delitem__(self, key):
        if key:
            self.major = None
        else:
            self.minor = None

    def __str__(self):
        return str(self.item)

    def get_list(self):
        return [self, *self.major.get_list(), *self.minor.get_list()]

root = Node(0)
root.add(1, 0)
root[0].add(2, 0)
root[0][0].add(3, 0)
root.add(-1, 1)
root.add(-2, 1)
root.add(-3, 1)
root[0].add(1.5, 0)
