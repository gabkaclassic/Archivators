import json
import pickle
from os import walk, remove, sep
from os.path import join, exists, isdir, isfile
from .file_utils import File, modes, bytes
from lab_3.utils import HuffmanCompression, IntervalCompressor


class Encoder:

    def __init__(self, extension='mrp', version='1.0.0', mode=modes['none']):
        self.extension = extension
        self.version = version
        self.mode = mode
        if self.mode == modes['huff']:
            self.version = '2.0.0'
        if self.mode == modes['interval']:
            self.version = '3.0.0'

        self.modes = []
        self.sizes = []
        self.paths = []
        self.codes = []
        self.encoded_mode = None

    def _input_files(self):

        path = input('Enter path/file(s): ')
        while not exists(path):
            path = input('Enter existing path/file(s): ')

        return path.split()

    def _output_file(self):
        path = input('Enter output path with filename: ')
        path = path.replace('.mrp', '') + '.mrp'
        return path

    def _request_mode(self, rel, full_path, files):
        mode = self.mode if self.encoded_mode else 0
        if not self.encoded_mode:
            try:
                mode = int(input(f'Mode for ({rel}): '))
            except:
                pass
        self.modes.append(mode)

        with open(full_path, 'rb') as current_file:
            codes, content, size = self._get_file_content(current_file, mode)
            if codes is None:
                print(len(content))
                file = File(content=content, abs_path=full_path, rel_path=rel)
            elif size is None:
                file = File(content=content, codes=codes, abs_path=full_path, rel_path=rel)
            else:
                file = File(content=pickle.dumps(content), codes=(codes, size), abs_path=full_path, rel_path=rel)

            files.append(file)
            self.sizes.append(file.size)
            self.codes.append(file.codes)
            self.paths.append(rel)

    def _search_files(self, paths):
        files = []
        for path in paths:
            if isdir(path):
                for root, subdirectories, file_list in walk(path):
                    for file in file_list:
                        full_path = join(root, file)
                        rel = full_path.replace(path, '')[1:].replace('\n', '')
                        self._request_mode(rel, full_path, files)
            elif isfile(path):
                rel = path.split(sep)[-1]
                self._request_mode(rel, path, files)

        return files

    def _get_file_content(self, current_file, mode):

        if int(mode) == modes['none']:
            return None, current_file.read(), None
        elif int(mode) == modes['huff']:
            data = current_file.read()
            compressor = HuffmanCompression()
            compressed_data = compressor.compress(data)
            return json.dumps(compressor.reverse_mapping), compressed_data if len(compressed_data) <= len(
                data) else data, None
        elif int(mode) == modes['interval']:
            data = current_file.read()
            compressor = IntervalCompressor()
            compressed_data, frequencies, size = compressor.compress(data)
            frequencies = { key: str(value) for key, value in frequencies.items() }
            return frequencies, compressed_data, size

    def _get_mode(self):
        split = input('Split mode: ') in ['y', 'yes', '1']
        if not split:
            self.mode = input('Encoding mode: ').replace('huff', '1').replace('none', '0').replace('interval', '3')
        return not split

    def create_archive(self):
        paths = ['/home/errodion/PycharmProjects/EncodeLabs/files/test/1.txt',]
                 # '/home/errodion/PycharmProjects/EncodeLabs/files/__init__.py']  # self._input_files()
        self.encoded_mode = self._get_mode()
        files = self._search_files(paths)
        print(self.modes)
        header = bytes(
            f'{self.extension}|{self.version}|{",".join(map(str, self.modes))}|{",".join(map(str, self.sizes))}|{",".join(self.paths)}|{json.dumps(self.codes)}\n')

        output_file = '/home/errodion/PycharmProjects/EncodeLabs/archives/a.mrp'  # self._output_file()
        if exists(output_file):
            remove(output_file)
        with open(output_file, 'wb') as output:
            output.write(header)
            for file in files:
                output.write(file.content)
        print('Success created')
