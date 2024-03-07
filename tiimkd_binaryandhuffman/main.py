import math
from collections import Counter
from bitarray import bitarray


def open_and_read_file(file_name):
    with open(file_name, 'r') as file:
        return file.read()


def find_unique_chars(string):
    string = string.lower()
    result = set(string)
    return result


def calculate_bits_for_alphabet(chars):
    num_unique_chars = len(chars)
    minimum_bits = math.ceil(math.log2(num_unique_chars))
    return minimum_bits


def assign_bit_representation(chars, bits):
    result = {}
    char_list = enumerate(chars)
    for index, char in char_list:
        binary_repr = format(index, f'0{bits}b')
        result[char] = binary_repr

    return result


def compress_text(text, bit_representation):
    compressed_text = ''.join(bit_representation.get(char, '') for char in text)
    compressed_bits = bitarray(compressed_text)
    return compressed_bits


def decode_bitarray_2(bits, bit_rep, num_bits):
    char_dict = {v: k for k, v in bit_rep.items()}

    decoded_string = ''
    for i in range(0, len(bits), num_bits):
        chunk = bits[i:i + num_bits]
        chunk_str = chunk.to01()
        if chunk_str in char_dict:
            decoded_string += char_dict[chunk_str]

    return decoded_string


def count_bits_in_string(input_string):
    bits = bitarray()
    bits.frombytes(input_string.encode('utf-8'))
    num_bits = len(bits)
    return num_bits


def calculate_char_ratios(input_string):
    text_length = len(input_string)
    char_count = Counter(input_string)
    char_ratios = [(char, count / text_length) for char, count in char_count.items()]
    return char_ratios


def save_bitarray_to_file(bit_array, file_path):
    other = len(bit_array) % 8
    bytes_data = bit_array.tobytes()

    padding = 8 - other
    bytes_data += bytes([padding])

    with open(file_path, 'wb') as file:
        file.write(bytes_data)


def remove_last_bits(bit_array, count):
    if 0 < count <= len(bit_array):
        del bit_array[-count:]


def open_file_as_bitarray(file_path):
    bit_array = bitarray()
    with open(file_path, 'rb') as file:
        bytes_data = file.read()

    if bytes_data:
        bit_array = bitarray(endian='big') # most significant bit in front
        bit_array.frombytes(bytes_data)
        padding = bit_array[-8:].tobytes()[0]
        remove_last_bits(bit_array, padding + 8)
    return bit_array


def entropy(data):
    data_counts = Counter(data)
    total_count = len(data)
    entropy_val = 0.0
    for count in data_counts.values():
        probability = count / total_count
        entropy_val -= probability * math.log2(probability)
    return entropy_val

# =====================================================================================


class Node:
    def __init__(self, value, frequency):
        self.value = value
        self.freq = frequency
        self.left = None
        self.right = None


def build_huffman_tree(character_ratios):
    nodes = [Node(char, ratio) for char, ratio in character_ratios]

    while len(nodes) > 1:
        nodes.sort(key=lambda x: x.freq)
        left = nodes.pop(0)
        right = nodes.pop(0)

        parent = Node(left.value + right.value, left.freq + right.freq)
        parent.left = left
        parent.right = right
        nodes.append(parent)
    return nodes[0]


def generate_huffman_codes(root):
    huffman_codes = {}

    def assign(node, code=''):
        if node:
            if not node.left and not node.right:
                huffman_codes[node.value] = code
            assign(node.left, code + '0')
            assign(node.right, code + '1')
    assign(root)
    return huffman_codes


def decode_bitarray(encoded_bits, huffman_codes):
    decoded_text = ''
    code = bitarray()
    reversed_codes = {v: k for k, v in huffman_codes.items()}

    for bit in encoded_bits:
        code.append(bit)
        code_str = code.to01()
        if code_str in reversed_codes:
            decoded_text += reversed_codes[code_str]
            code = bitarray()
    return decoded_text


def average_code_length_from_huffman(root, character_ratios):
    huffman_codes = generate_huffman_codes(root)

    average_length = 0
    for character, ratio in character_ratios:
        if character in huffman_codes:
            code_length = len(huffman_codes[character])
            average_length += ratio * code_length
    return average_length


if __name__ == '__main__':

    # binary compression
    input_string = open_and_read_file("norm_wiki_sample.txt")
    unique_chars = find_unique_chars(input_string)
    minimum_bits = calculate_bits_for_alphabet(unique_chars)
    bit_repr = assign_bit_representation(unique_chars, minimum_bits)
    compressed = compress_text(input_string, bit_repr)

    save_bitarray_to_file(compressed, "norm_wiki_sample.bin")
    original_bitarray = open_file_as_bitarray("norm_wiki_sample.bin")
    decompressed_bits = decode_bitarray_2(original_bitarray, bit_repr, minimum_bits)

    if input_string == decompressed_bits:
        print("Dekompresja udana")

        original_bits = count_bits_in_string(input_string)
        compressed_bits = len(bitarray(compressed))
        average_length = sum([len(bit_repr[char]) for char in input_string]) / len(input_string)

        print(f"Stopien kompresji: {original_bits / compressed_bits}")
        print(f"Efektywnosc kodowania: {entropy(input_string) / average_length}")
    else:
        print("Dekompresja nieudana")


    # huffmans compression
    input_string = open_and_read_file("norm_wiki_sample.txt")
    character_ratios = calculate_char_ratios(input_string)
    root = build_huffman_tree(character_ratios)
    huffman_codes = generate_huffman_codes(root)
    compressed = compress_text(input_string, huffman_codes)
    save_bitarray_to_file(compressed, "norm_wiki_sample.bin")
    original_bitarray = open_file_as_bitarray("norm_wiki_sample.bin")
    decompressed_bits = decode_bitarray(original_bitarray, huffman_codes)

    if input_string == decompressed_bits:
        print("Dekompresja udana")

        original_bits = count_bits_in_string(input_string)
        compressed_bits = len(bitarray(compressed))

        print(f"Stopien kompresji: {original_bits / compressed_bits}")
        print(f"Efektywnosc kodowania: {entropy(input_string) / average_code_length_from_huffman(root, character_ratios)}")
    else:
        print("Dekompresja nieudana")

