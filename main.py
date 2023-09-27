
def lab_1():
    from lab_1.encoder import Encoder
    from lab_1.decoder import Decoder
    encoder = Encoder()
    decoder = Decoder()
    encoder.create_archive()
    decoder.read_archive()

def lab_2():
    from lab_2 import counter

def lab_3():
    from lab_3.utils import IntervalCompressor
    compressor = IntervalCompressor()
    data = open('files/test/test1/test2/Resume.pdf', 'rb').read()
    compressed, frequencies, size = compressor.compress(data)
    decompressed = compressor.decompress(compressed, frequencies, size)
    open('test.pdf', 'wb').write(decompressed)
lab_1()
# lab_3()