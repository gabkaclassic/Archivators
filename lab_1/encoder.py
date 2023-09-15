from os import walk, remove, sep
from os.path import join, exists, isdir, isfile
from .file_utils import File, modes, bytes, to_str

class Encoder:

    def __init__(self, extension='mrp', version='1.0.0', mode=modes['none']):
        self.extension = extension
        self.version = version
        self.mode = mode

    def _input_files(self):

        path = input('Enter path/file(s): ')
        while not exists(path):
            path = input('Enter existing path/file(s): ')

        return path.split()


    def _output_file(self):
        path = input('Enter output path with filename: ')
        path = path.replace('.mrp', '') + '.mrp'
        return path

    def _search_files(self, paths):
        files = []
        print(paths)
        for path in paths:

            if isdir(path):
                for root, subdirectories, file_list in walk(path):
                    for file in file_list:
                        full_path = join(root, file)
                        rel = join(root.replace(path if path.endswith('/') else path + '/', ""), file)
                        print(full_path)
                        with open(full_path, 'rb') as current_file:
                            current_file = File(content=current_file.readlines(), abs_path=full_path, rel_path=rel)
                            files.append(current_file)
            elif isfile(path):
                rel = path.split(sep)[-1]

                with open(path, 'rb') as current_file:
                    current_file = File(content=current_file.readlines(), abs_path=path, rel_path=rel)
                    files.append(current_file)
        return files

    def create_archive(self):
        paths = ['/home/errodion/PycharmProjects/EncodeLabs/files', '/home/errodion/Projects/Encoding/otik/labs-files', '/home/errodion/PycharmProjects/EncodeLabs/files/__init__.py'] #self._input_files()
        files = self._search_files(paths)
        archive_size = len(files)
        header = bytes(f'{self.extension}|{self.version}|{self.mode}|{archive_size}\n')

        output_file = '/home/errodion/PycharmProjects/EncodeLabs/archives/a.mrp' #self._output_file()
        if exists(output_file):
            remove(output_file)
        with open(output_file, 'wb') as output:
            output.write(header)
            for file in files:
                output.write(bytes(f'\n{file.size}\n{file.rel_path}\n'))
                output.writelines(file.content)
        print('Success created')





