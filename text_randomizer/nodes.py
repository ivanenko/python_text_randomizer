import re
from random import shuffle, choice


class Node(object):

    def __init__(self, parent=None):
        self._subnodes = []

        self.parent = parent
        if self.parent:
            self.parent.add_child(self)

    def add_child(self, node):
        self._subnodes.append(node)

    def get_indexes(self):
        indexes = []
        for node in self._subnodes:
            indexes.extend(node.get_indexes())

        return indexes

    def concat(self, index):
        return None

    def variants_number(self):
        res = 0
        for n in self._subnodes:
            res += n.variants_number()

        return res


class StringNode(Node):

    def __init__(self, parent, index):
        super(StringNode, self).__init__(parent)
        self._str_indexes = [[index, index+1], ]

    def get_indexes(self):
        return self._str_indexes

    def concat(self, index):
        if self._str_indexes and self._str_indexes[-1][1] == index:
            self._str_indexes[-1][1] += 1
        else:
            self._str_indexes.append([index, index+1])

        return self

    def variants_number(self):
        return 1


class SeriesNode(Node):

    def concat(self, index):
        return StringNode(self, index)

    def variants_number(self):
        res = 1
        for n in self._subnodes:
            res *= n.variants_number()

        return res


class SynonymsNode(Node):

    def __init__(self, parent):
        super(SynonymsNode, self).__init__(parent)
        self._used_nodes = []

    def get_indexes(self):
        if not self._used_nodes:
            self._used_nodes = list(range(0, len(self._subnodes)))

        random_index = choice(self._used_nodes)
        self._used_nodes.remove(random_index)

        return self._subnodes[random_index].get_indexes()


class MixingNode(Node):

    def __init__(self, parent=None, separator=None):
        super(MixingNode, self).__init__(parent)
        self.separator = separator

    def get_indexes(self):
        shuffle(self._subnodes)
        result = []
        for node in self._subnodes:
            result.extend(node.get_indexes())
            result.append(self.separator)

        # remove last separator item
        result = result[:-1]
        return result

    def variants_number(self):
        res = 1
        for i in range(2, len(self._subnodes)+1):
            res *= i

        for n in self._subnodes:
            res *= n.variants_number()

        return res


class FunctionNode(Node):

    def __init__(self, parent, function, *args):
        super(FunctionNode, self).__init__(parent)

        if type(function) == dict:
            self._callable = function['callable']
            _coerce = function['coerce']
        else:
            self._callable = function
            _coerce = str

        self._args = [_coerce(a) for a in args]

    def get_indexes(self):
        return str(self._callable(*self._args))

    def variants_number(self):
        return 1