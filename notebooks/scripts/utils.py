
from typing import List, Tuple


def sum32(a: int, b: int) -> int:
    # Suma mod 2^32
    return (a + b) & ((1 << 32) - 1)

assert(sum32(2**32, 3) == 3), "Error"

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


def split_words(n: int, word_size: int, word_num: int) -> List[int]:
    """Dvidide un número en palabras

    Args:
        n (int): _description_
        word_size (int): tamaño de la palabra en bytes
        word_num (int): cantidad de palabras

    Returns:
        List[int]: Lista de palabras
    """
    size = word_size * word_num
    
    n = n.to_bytes(size, byteorder='big')
    return [int.from_bytes(n[i:i+word_size], byteorder='big') for i in range(0, len(n), word_size)]

assert(split_words(0x1A38B5EE, 1, 4) == [0x1A, 0x38, 0xB5, 0xEE])
assert(split_words(0x2b7e151628aed2a6abf7158809cf4f3c, 4, 4) == [0x2b7e1516, 0x28aed2a6, 0xabf71588, 0x09cf4f3c])
assert(split_words( 0x8e73b0f7da0e6452c810f32b809079e562f8ead2522c6b7b, 4, 6) == [0x8e73b0f7, 0xda0e6452, 0xc810f32b, 0x809079e5, 0x62f8ead2, 0x522c6b7b])
assert(split_words(0x603deb1015ca71be2b73aef0857d77811f352c073b6108d72d9810a30914dff4, 4, 8) == [0x603deb10, 0x15ca71be, 0x2b73aef0, 0x857d7781, 0x1f352c07, 0x3b6108d7, 0x2d9810a3, 0x0914dff4])


def join_words(words: List[int], word_size: int) -> int:
    """Una una lista de palabras en un solo número

    Args:
        words (List[int]): Lista de palabras
        word_size (int): tamaño de la palabra (en bytes)

    Returns:
        int: Entero
    """
    return int("".join([w.to_bytes(word_size, "big").hex() for w in words]), 16)

assert(join_words([0x1A, 0x38, 0xB5, 0xEE], 1) == 0x1A38B5EE)
assert(join_words([0x2b7e1516, 0x28aed2a6, 0xabf71588, 0x09cf4f3c], 4) == 0x2b7e151628aed2a6abf7158809cf4f3c)
assert(join_words([0x8e73b0f7, 0xda0e6452, 0xc810f32b, 0x809079e5, 0x62f8ead2, 0x522c6b7b], 4) == 0x8e73b0f7da0e6452c810f32b809079e562f8ead2522c6b7b)
assert(join_words([0x603deb10, 0x15ca71be, 0x2b73aef0, 0x857d7781, 0x1f352c07, 0x3b6108d7, 0x2d9810a3, 0x0914dff4], 4) == 0x603deb1015ca71be2b73aef0857d77811f352c073b6108d72d9810a30914dff4)