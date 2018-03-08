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

    def get_text(self, template):
        res = ' '.join([child.get_text(template) for child in self._subnodes])
        return re.sub('\s+', ' ', res)
        #return res

    def concat(self, index):
        return None


class StringNode(Node):

    def __init__(self, parent, index):
        super(StringNode, self).__init__(parent)
        self._str_indexes = [[index, index+1], ]

    def get_text(self, template):
        return ''.join([template[i[0]: i[1]] for i in self._str_indexes])

    def concat(self, index):
        if self._str_indexes and self._str_indexes[-1][1] == index:
            self._str_indexes[-1][1] += 1
        else:
            self._str_indexes.append([index, index+1])

        return self


class SeriesNode(Node):

    def get_text(self, template):
        return ' '.join([node.get_text(template) for node in self._subnodes])

    def concat(self, index):
        return StringNode(self, index)


class SynonymsNode(Node):

    def __init__(self, parent):
        super(SynonymsNode, self).__init__(parent)
        self._used_nodes = []

    def get_text(self, template):
        if not self._used_nodes:
            self._used_nodes = list(range(0, len(self._subnodes)))

        random_index = choice(self._used_nodes)
        self._used_nodes.remove(random_index)

        return self._subnodes[random_index].get_text(template)


class MixingNode(Node):

    def __init__(self, parent=None, separator=' '):
        super(MixingNode, self).__init__(parent)
        self.separator = separator

    def get_text(self, template):
        shuffle(self._subnodes)
        texts = [c.get_text(template) for c in self._subnodes]
        return self.separator.join(texts)


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

    def get_text(self, template):
        return str(self._callable(*self._args))