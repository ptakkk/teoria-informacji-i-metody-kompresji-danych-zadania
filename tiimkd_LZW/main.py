import struct


def reset_dictionary():
    return {bytes([i]): i for i in range(256)}


def compress(data, max_bit_length):
    with open(data, 'rb') as file:
        data = file.read()
    max_dict_size = 4096
    dictionary = reset_dictionary()
    next_code = 256
    bit_length = 9
    compressed_data = bytearray()
    buffer = b''
    for byte in data:
        new_buffer = buffer + bytes([byte])
        if new_buffer in dictionary:
            buffer = new_buffer
        else:
            compressed_data.extend(struct.pack('>H', dictionary[buffer]))
            if next_code < max_dict_size:
                dictionary[new_buffer] = next_code
                next_code += 1
            buffer = bytes([byte])
            if next_code >= 2**bit_length and bit_length < max_bit_length:
                bit_length += 1
    if buffer:
        compressed_data.extend(struct.pack('>H', dictionary[buffer]))
    return compressed_data


def decompress(compressed_data, max_dict_size=4096, max_bit_length=12):
    dictionary = reset_dictionary()
    next_code = 256
    bit_length = 9
    decompressed_data = bytearray()
    buffer = bytes([compressed_data[0]])
    decompressed_data.extend(buffer)
    entry = None
    for i in range(2, len(compressed_data), 2):
        code = struct.unpack('>H', compressed_data[i:i+2])[0]
        if code in dictionary.values():
            entry = get_entry(dictionary, code)
        elif code == next_code:
            entry = buffer + bytes([buffer[0]])
        if entry:
            decompressed_data.extend(entry)
            if next_code < max_dict_size:
                dictionary[next_code] = buffer + bytes([entry[0]])
                next_code += 1
            buffer = entry
            if next_code >= 2**bit_length and bit_length < max_bit_length:
                bit_length += 1
        else:
            raise ValueError("Invalid compressed data")
    return bytes(decompressed_data)


def get_entry(dictionary, code):
    for key, value in dictionary.items():
        if value == code:
            return key

# ==============================================


class Node:
    def __init__(self, value, frequency):
        self.value = value
        self.freq = frequency
        self.left = None
        self.right = None


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


def calculate_freq(data):
    freq_dict = {}
    for char in data:
        if char not in freq_dict:
            freq_dict[char] = 1
        else:
            freq_dict[char] += 1
    return freq_dict


def huffman_encode(input_data, code_map):
    return ''.join([code_map[char] for char in input_data])


def main():
    print('Kodowanie LZW')
    compress("lena.bmp", 12)
    compress("lena.bmp", 18)
    compress("lena.bmp", 12)
    compress("norm_wiki_sample.txt", 12)
    compress("norm_wiki_sample.txt", 18)
    compress("norm_wiki_sample.txt", 12)
    compress("wiki_sample.txt", 12)
    compress("wiki_sample.txt", 18)
    compress("wiki_sample.txt", 12)

if __name__ == "__main__":
    main()
