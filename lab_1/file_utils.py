import pickle
from decimal import Decimal

modes = {
    'none': 0,
    'huff': 1,
    'interval': 2,
}


class File:

    def __init__(self, content=None, abs_path='', rel_path='', codes=None):

        if content is None:
            content = []

        self.codes = codes
        self.content = content
        self.abs_path = abs_path
        self.rel_path = rel_path
        self.size = 0
        self._get_size()

    def _get_size(self):
        if isinstance(self.content, Decimal):
            self.size = len(pickle.dumps(self.content))
        else:
            self.size = len(self.content)

    def _get_string_size(self, string):
        return len(bytes(string))

def bytes(value):
    return value.encode('utf-8')


def to_int(value):
    return int(to_str(value))


def to_str(value):
    if not isinstance(value, str):
        return value.decode('utf-8')
    return value
