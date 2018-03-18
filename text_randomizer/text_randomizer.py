import uuid
import datetime
from random import random, randint
from .nodes import Node, SeriesNode, StringNode, MixingNode, SynonymsNode, FunctionNode
#from nodes import Node, SeriesNode, StringNode, MixingNode, SynonymsNode, FunctionNode


class TextRandomizer(object):

    functions = {
        'RANDINT': {'callable': randint, 'coerce': int},
        'RANDOM': random,
        'UUID': uuid.uuid4,
        'NOW': lambda p: datetime.datetime.now().strftime(p)
    }

    def __init__(self, template, parse=True):
        self.tree = None
        self.template = template

        if parse:
            self.parse()

    def add_function(self, name, func):
        self.functions[name] = func

    def get_text(self):
        if self.tree:
            result = []
            for indexes in self.tree.get_indexes():
                if indexes:
                    if type(indexes) == list:
                        result.append(self.template[indexes[0]: indexes[1]])
                    else:
                        result.append(indexes)
                else:
                    result.append(" ")

            return ''.join(result)
            #return re.sub('\s+', ' ', res)
        else:
            raise Exception('Template not parsed yet')

    def variants_number(self):
        if self.tree:
            return self.tree.variants_number()
        else:
            raise Exception('Template not parsed yet')

    def reset(self):
        self.tree = None

    def parse(self):
        i = 0
        self.tree = Node()
        current_node = SeriesNode(self.tree)
        while i < len(self.template):
            if self.template[i] == '\\':
                current_node = current_node.concat(i+1)
                i += 2
                continue

            elif self.template[i] == '[':
                separator, i = self._get_separator(i)
                p = self._closest_series_node(current_node)
                current_node = MixingNode(p, separator)
                current_node = SeriesNode(current_node)

            elif self.template[i] == '{':
                p = self._closest_series_node(current_node)
                current_node = SynonymsNode(p)
                current_node = SeriesNode(current_node)

            elif self.template[i] == '}' or self.template[i] == ']':
                p = self._closest_series_node(current_node)
                current_node = p.parent.parent
                if not current_node:
                    # on the top of tree - 'str1 } {a|b}' or 'str2 ] [a|b]'
                    current_node = current_node.concat(i)

            elif self.template[i] == '|':
                p = self._closest_series_node(current_node)
                if isinstance(p.parent, (MixingNode, SynonymsNode)):
                    current_node = SeriesNode(p.parent)
                else:
                    # on the top of tree - 'bla1 | bla2'
                    current_node = current_node.concat(i)

            elif self.template[i] == '$':
                start_func = i
                func_name, i = self._get_function_name(i)
                func_args, i = self._get_function_args(i)
                func = self.functions.get(func_name, None)
                if func:
                    current_node = self._closest_series_node(current_node)
                    FunctionNode(current_node, func, *func_args)
                    continue
                else:
                    i = start_func
                    current_node = current_node.concat(i)

            else:
                # getting StringNode here
                current_node = current_node.concat(i)

            i += 1

    def _get_function_name(self, i):
        i += 1
        start = i
        while self.template[i].isalnum() or self.template[i] == '_':
            i += 1

        func_name = self.template[start: i]
        return func_name, i

    def _get_function_args(self, i):
        args = []
        if self.template[i] == '(':
            i += 1
            start = i
            while self.template[i] != ')':
                i += 1
            args_string = self.template[start: i]
            i += 1
            if len(args_string.strip()) > 0:
                args = args_string.split(',')

        return args, i

    def _closest_series_node(self, current_node):
        if type(current_node) == SeriesNode:
            return current_node
        elif type(current_node) == StringNode:
            return current_node.parent
        else:
            return None

    def _get_separator(self, i):
        separator = None
        if (i+1) < len(self.template) and self.template[i+1] == '+':
            i += 2
            start = i
            while (i+1) < len(self.template) and self.template[i] != '+':
                i += 1
            separator = [start, i]

        return separator, i


if __name__ == '__main__':

    #template = 'sss [a|dd [+=+b1|b2]] end'
    #template = '[+==+ooo|www]|asd| [aaa|$RANDINT(1,10)|{d1|d2|[aaaaa|zzzzzz]}] sss  zzz'
    #template = '[+==+ooo|www] asd [aaa|$RANDINT(1,10)|{d1|d2|[aaaaa|zzzzzz]}] sss  zzz'
    template = '{a|b|c} $DDD ooo $AAA(1,5) www $NOW(%H:%M:%S) end'

    text_rnd = TextRandomizer(template, parse=False)
    text_rnd.add_function('AAA', {'callable': lambda x, y: randint(x,y), 'coerce': int})
    text_rnd.add_function('DDD', {'callable': lambda: 'test_string', 'coerce': str})
    text_rnd.parse()
    print(text_rnd.get_text())
    print(text_rnd.get_text())
    print(text_rnd.get_text())
    print(text_rnd.get_text())