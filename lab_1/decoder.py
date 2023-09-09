from os.path import isdir, isfile, dirname, join
from os import makedirs
import re
from .file_utils import modes, to_int, to_str


class Decoder:

    def read_archive(self):
        path = 'archives/a.mrp' #self._input_path()
        output = 'outputs/info' #self._output_path()

        with open(path, 'rb') as archive:
            content = archive.readlines()

        header = to_str(content[0])
        offset = 2
        if self._check_header(header):
            if self.decode_mode[0] == 0:
                for number_file in range(self.archive_size):
                    print(content[offset])
                    try:
                        size = to_int(to_str(content[offset]))
                    except:
                        offset -= 1
                        size = to_int(to_str(content[offset]))
                    offset += 1

                    rel_path = to_str(content[offset])
                    print(rel_path)
                    offset += 1

                    file_content = content[offset: offset + size]
                    offset += size + 1

                    path_dir = join(output, dirname(rel_path))
                    path_file = join(output, rel_path)
                    makedirs(path_dir, exist_ok=True)
                    with open(path_file, 'wb') as new_file:
                        r = new_file.writelines(file_content)
                        print(r)
    def _check_header(self, header):
        metadata = header.split('|')
        self.format = to_str(metadata[0])
        self.version = to_str(metadata[1])
        self.decode_mode = [to_int(to_str(mode)) for mode in metadata[2].split(',')]
        self.archive_size = to_int(metadata[3])

        return self._check_version() \
            and self._check_decode_mode() \
            and self._check_archive_size()

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

    def _check_archive_size(self):
        return self.archive_size > 0

    def _check_decode_mode(self):
        for mode in self.decode_mode:
            if mode not in modes.values():
                return False
        return True
