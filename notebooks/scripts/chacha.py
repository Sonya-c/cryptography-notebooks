
from typing import Tuple, List
from utils import split_words, join_words, text_to_int, sum32

class Chacha:
    c = [0x61707865, 0x3320646e, 0x79622d32, 0x6b206574]
    L = 1

    def pad(self, s: int, j: int, n: int) -> int:
        """Una función que combina una semilla s de 256 bits, un contador j de 64 bits (j0 y j1 de 32bits), y un ruido (nonce) n de 64 bits (n0 y n1 de 32 bits) para formar un bloque de 512 bits

        Args:
            s: Seed (256 bits, 8 palabras de 32 bits)
            j: counter (64 bits)
            n: Nonce (64 bits)

        Returns:
            512 bits (16 palabras de 32 bits)
        """

        s = split_words(s, 32 // 8, 8)
        j = split_words(j, 32 // 8, 2)
        n = split_words(n, 32 // 8, 2)

        return [
            self.c[0], self.c[1], self.c[2], self.c[3],
            s[0], s[1], s[2], s[3],
            s[4], s[5], s[6], s[7],
            j[0], j[1], n[0], n[1]
        ]
    
    def rot(self, w: int, r: int) -> int: 
        """No se queda hace

        Args:
            w: palabra 
            r: No me acuerdo
        """

        mask = 0xffffffff
        return ((w << r) & mask) | (w >> (32 - r))

    def QR(self, a: int, b: int, c: int, d: int) -> Tuple[int, int, int, int]:
        """Cuarto de ronda

        Args:
            a (int): palabra
            b (int): palabra
            c (int): palabra
            d (int): palabra

        Returns:
            Tuple[int, int, int, int]: sequencia de 4 palabras
        """
        a = sum32(a, b)
        d = d ^ a 
        d = self.rot(d, 16)

        c = sum32(c, d)
        b = b ^ c
        b = self.rot(b, 12)

        a = sum32(a, b)
        d = d ^ a
        d = self.rot(d, 8)

        c = sum32(c, d)
        b = b ^ c
        b = self.rot(b, 7)
        
        return a, b, c, d

    def round(self, i):
        i[0], i[4], i[8], i[12] = self.QR(i[0], i[4], i[8], i[12])
        i[1], i[5], i[9], i[13] = self.QR(i[1], i[5], i[9], i[13])
        i[2], i[6], i[10], i[14] = self.QR(i[2], i[6], i[10], i[14])
        i[3], i[7], i[11], i[15] = self.QR(i[3], i[7], i[11], i[15])

        i[0], i[5], i[10], i[15] = self.QR(i[0], i[5], i[10], i[15])
        i[1], i[6], i[11], i[12] = self.QR(i[1], i[6], i[11], i[12])
        i[2], i[7], i[8], i[13] = self.QR(i[2], i[7], i[8], i[13])
        i[3], i[4], i[9], i[14] = self.QR(i[3], i[4], i[9], i[14])

        return i

    def perm(self, x: int, ROUNDS: int = 20): 
        """Permutación

        Args:
            x: 512 bits (16 palabras 32 bits)
            ROUNDS: Número de rondas
                - 20 (ChaCha20/20)
                - 8 (ChaCha20/8)
                - 12 (ChaCha20/12)
                
        Returns:
            512 bits (16 palabras 32 bits)
        """
        assert(ROUNDS in [8, 12, 20]), "Invalid number of rounds"
        
        i = x.copy()
        
        for _ in range(0, ROUNDS, 2): 
            self.round(i)
        return i

    def G(self, s: int, n: int):
        r = [0]*self.L

        for j in range(self.L):
            h = self.pad(s, j, n) # 512 bits
            pi = self.perm(h) # 512 bits

            r[j] = [0]*16
            for i in range(16):
                r[j] = join_words(pi, 32) + join_words(h, 32)
            
        return r
    
    def encrypt(self, k, n, m): 
        keys = self.G(k, n)
        return m ^ keys[0]
    
    def decrypt(self, k, n, c):
        keys = self.G(k, n)
        return c ^ keys[0]


if __name__ == '__main__':
    chacha = Chacha()

    assert(
        chacha.pad(0x47f515b1dd45f8d5aceea73b52971be21f7b4b3355a35fd6a2799898ed2f8c97,
        0x722d9d570ac23201,
        0xed539cd99e1d2f20) ==
        
        [0x61707865, 0x3320646e, 0x79622d32, 0x6b206574,
        0x47f515b1, 0xdd45f8d5, 0xaceea73b, 0x52971be2,
        0x1f7b4b33, 0x55a35fd6, 0xa2799898, 0xed2f8c97,
        0x722d9d57, 0x0ac23201, 0xed539cd9, 0x9e1d2f20]
    ), "Pad test failed"

    assert(
        chacha.QR(0xc2619378, 0xecdaec96, 0xe62bd0c8, 0x2b61be56) ==
        (0x9ad7bc93, 0x130fa62c, 0xb3bd23c9, 0x8f38cea4)
    ), "QR test failed"

    s = 0x47f515b1dd45f8d5aceea73b52971be21f7b4b3355a35fd6a2799898ed2f8c97
    j = 0x722d9d570ac23201
    n = 0xed539cd99e1d2f20

    _pad = chacha.pad(s, j, n)

    assert(join_words(chacha.perm(_pad), 32 // 8) == 0xc9ead123f6eee2042ce8442128342dcdddec68c9446ec082de92f642f498c0a843d9d8d27c44c2bd1945edeb3411fa78fffb0e607ec9ec17b7a5cfae23663818), "Permutation test failed"

    s = 0x112233445566778899aabbccddeeff00
    n = 0x0123456789abcdef
    m = text_to_int("Hola mundo!")
    assert(chacha.decrypt(s, n, chacha.encrypt(s, n, m)) == m), "Error"