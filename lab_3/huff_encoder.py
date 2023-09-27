from lab_1.encoder import Encoder


class HuffEncoder(Encoder):

    def _get_file_content(self, current_file):
        with open(current_file, 'r') as file:
            data = file.read().rstrip()

        return data

    def _get_encode_mode(self):
        return 'huff'
    