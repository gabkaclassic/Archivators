import json
import pickle
from os.path import isfile, dirname, join, exists
from os import makedirs
import re
from .file_utils import modes, to_str
from lab_3.utils import HuffmanCompression, IntervalCompressor
from decimal import Decimal


class Decoder:
    available_versions=[
        '1.0.0',
        '2.0.0',
    ]
    def __init__(self, mode=modes['none']):
        self.mode = mode
        self.sizes = []
        self.modes = []
        self.paths = []
        self.codes = []

    def read_archive(self):
        path = 'archives/a.mrp' #self._input_path()
        output = 'outputs/info' #self._output_path()


        with open(path, 'rb') as archive:
            header = archive.readline().decode()
            if self._check_header(header):
                for ind in range(len(self.sizes)):
                    size = self.sizes[ind]
                    mode = self.modes[ind]
                    file_path = self.paths[ind]
                    codes = self.codes[ind]
                    data = [archive.read(1) for _ in range(size)] if mode == modes['huff'] else archive.read(size)
                    if int(mode) == modes['none']:
                        content = data
                    elif int(mode) == modes['huff']:
                        content = HuffmanCompression(codes).decompress(data)
                    elif int(mode) == modes['interval']:
                        data = Decimal(pickle.loads(data))
                        frequencies = { int(key): Decimal(value) for key, value in codes[0].items() }
                        size = codes[1]
                        content = IntervalCompressor().decompress(data, frequencies, size)
                    full_path = join(output, file_path)
                    if not exists(dirname(full_path)):
                        makedirs(dirname(full_path), exist_ok=True)

                    with open(full_path, 'wb') as file:
                        file.write(content)

    def _check_header(self, header):
        metadata = header.split('|')
        self.format = to_str(metadata[0])
        if self.format != 'mrp':
            raise Exception("Invalid header format")
        self.version = to_str(metadata[1])
        # print(self.version)
        if self.version not in Decoder.available_versions:
            raise Exception('Invalid version')
        print(metadata[2])
        self.modes = list(map(int, metadata[2].split(',')))
        self.sizes = list(map(int, metadata[3].split(',')))
        self.paths = metadata[4].split(',')
        self.codes = json.loads(metadata[5])

        return self._check_version()
    def _output_path(self):
        path = input('Enter output path: ')

        return path

    def _input_path(self):
        path = input('Enter archive path: ')
        while not isfile(path) or not path.endswith('.mrp'):
            path = input('Enter archive path: ')

        return path

    def _check_version(self):
        pattern = r'^\d+\.\d+\.\d+$'
        if re.match(pattern, self.version):
            return True
        return False

