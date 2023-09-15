import os
from collections import Counter
import math
import re

pattern = re.compile(r'[а-яА-ЯёЁ]')

def read_content(path, mode='all'):
    with open(path, 'rb') as file:
        content = file.read()

    if mode == 'all':
        return content
    elif mode == 'utf-8':
        return content.decode('utf-8')


def calculate_all(path):
    content = read_content(path)
    calculate_file_statistics(content)


def calculate_utf_8(path):
    content = read_content(path, mode='utf-8')
    calculate_file_statistics(content)


def calculate_file_statistics(content):
    file_length = len(content)

    symbol_frequencies = Counter(content)

    probabilities = {symbol: frequency / file_length for symbol, frequency in symbol_frequencies.items()}

    information_content = {symbol: -1 * (prob * math.log2(prob)) for symbol, prob in
                           probabilities.items()}

    total_info_bits = -sum([(prob * math.log2(prob)) for _, prob in
                           probabilities.items()])
    total_info_bytes = total_info_bits / 8

    sorted_alphabet = sorted(symbol_frequencies.items(), key=lambda x: x[0])

    sorted_frequencies = sorted(symbol_frequencies.items(), key=lambda x: x[1], reverse=True)

    print(f"File content length: {file_length}")
    print("Table (by letters):")

    print_table(sorted_alphabet, probabilities, information_content)
    print("\nTable (by frequency):")
    print_table(sorted_frequencies, probabilities, information_content)
    print("\nAmount of information:")
    print(f"bits: {total_info_bits}")
    print(f"bytes: {total_info_bytes}")


def analyze_file(path):
    octet_frequencies = Counter(read_content(path))

    # Наиболее частые октеты
    most_common_octets = octet_frequencies.most_common(4)

    # Наиболее частые октеты, не являющиеся кодами печатных символов ASCII
    non_printable_ascii_octets = [octet for octet, _ in octet_frequencies.most_common() if octet < 32 or octet > 126][
                                 :4]
    print(f"Octets: {[ c[0] for c in most_common_octets ]}")
    print(f"Octets (not ASCII): {non_printable_ascii_octets}")

    is_russian(octet_frequencies)


def print_table(symbol_frequencies, probabilities, information):
    print("Symbol\tFrequency\tProbabilities\tInformation")
    for symbol, frequency in symbol_frequencies:
        prob = round(probabilities[symbol], 10)
        info = round(information[symbol], 10)
        frequency = round(frequency, 10)
        print(f"{symbol}\t{frequency}\t{prob}\t{info}")


def is_russian(octet_frequencies):
    for encoding_name in ['utf-8', 'cp1251', 'koi8-r']:
        try:
            text = bytes(octet_frequencies.keys()).decode(encoding_name)
            if pattern.search(text):
                print(text)
                print(f"Russian text (encoding - {encoding_name})")
        except UnicodeDecodeError:
            continue


file_path = '/home/errodion/Projects/Encoding/otik/labs-files/Файлы в разных форматах/beep.ogg'
# file_path = '/home/errodion/Projects/Encoding/otik/labs-files/Файлы в формате простого текста — utf8/Rewards and Fairies, by Rudyard Kipling.txt'
# file_path = '/home/errodion/Projects/Encoding/otik/labs-files/Файлы в формате простого текста — кодировки разные/Алфавит — koi8r.txt'

if os.path.exists(file_path):
    print('---|ALL|---')
    calculate_all(file_path)
    # print('---|UTF-8|---')
    # calculate_utf_8(file_path)
    # analyze_file(file_path)
else:
    print("File not found")
