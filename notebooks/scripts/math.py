
# A word is an elment of 32 bits. THe sum of two word is mod 2**32

def sum32(a: int, b: int) -> int:
    # Suma mod 2^32
    return (a + b) & ((1 << 32) - 1)

assert(sum32(2**32, 3) == 3), "Error"


def rot(w: int, r: int) -> int: 
    """Rotate lest for 32 bits

    Args:
        w: word to rotate
        r: I dont remember
    """

    mask = 0xffffffff
    return ((w << r) & mask) | (w >> (32 - r)) 