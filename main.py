from lab_1.encoder import Encoder
from lab_1.decoder import Decoder

encoder = Encoder()
decoder = Decoder()
encoder.create_archive()
decoder.read_archive()
