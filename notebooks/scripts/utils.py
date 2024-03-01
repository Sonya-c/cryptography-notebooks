
from typing import List, Tuple

def text_to_int(string: str) -> int:
    # I copy this from StackOverFlow
    nchars = len(string)
    return sum(ord(string[byte])<<8*(nchars-byte-1) for byte in range(nchars))

assert(text_to_int("expa"[::-1]) == 0x61707865), "Error"


def int_to_text(integer: int) -> str:
    # I dont remmber where I found this
    result = ""
    while integer > 0:
        byte = integer & 0xFF
        result = chr(byte) + result
        integer >>= 8
    
    return result

assert("expa" == int_to_text(0x61707865)[::-1]), "Error"


# Chatgpt assited generated code 
# Do no ask me how it works

def to_words(value: int,
             word_size: int,
             words_num: int) -> List[int]:
    
    hex_string = hex(value)[2:]  # Remove '0x' prefix
    
    binary_string = bin(int(hex_string, 16))[2:].zfill(len(hex_string) * 4)  # Convert to binary
    padding_bits = word_size * words_num - len(binary_string)
    
    if padding_bits < 0:
        raise ValueError("Number of words specified is insufficient for the given value.")
    
    binary_string = binary_string.zfill(word_size * words_num)  # Add leading zeros for padding
    
    words = [int(binary_string[i:i+word_size], 2) for i in range(0, len(binary_string), word_size)]
    
    return words

assert(to_words(0x112233445566778899aabbccddeeff00, 32, 8) == [0x0, 0x0, 0x0, 0x0, 0x11223344, 0x55667788, 0x99aabbcc, 0xddeeff00]), "Error"


def from_words(words: List[int], word_size: int) -> int:
    binary_string = ''.join(format(word, f'0{word_size}b') for word in words)
    hex_string = hex(int(binary_string, 2))
    return int(hex_string, 16)

assert(0x112233445566778899aabbccddeeff00 == from_words([0x0, 0x0, 0x0, 0x0, 0x11223344, 0x55667788, 0x99aabbcc, 0xddeeff00], 32)), "Error"
