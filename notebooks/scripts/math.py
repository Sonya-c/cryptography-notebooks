
# A word is an elment of 32 bits. THe sum of two word is mod 2**32

def sum32(a: int, b: int) -> int:
    # Suma mod 2^32
    return (a + b) & ((1 << 32) - 1)

assert(sum32(2**32, 3) == 3), "Error"

