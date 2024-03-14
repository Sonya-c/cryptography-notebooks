
from typing import Tuple, List
from utils import split_words, join_words, text_to_int, sum32

class Salsa:
    c = [0x61707865, 0x3320646e, 0x79622d32, 0x6b206574]
    L = 1 

    def pad(self, s: int, j: int, n: int) -> int:
        """
        Es una función que combina una semilla $s$ de 256 bits con un contador $j$ de 64 bits (j0, j1 de 32 bits) y un ruido (nonce) de 64 bits (n0 y b1 de 31 bits) para formar un bloque de 512 bits
        
        Args:
            s: Seed (256 bits, 8 palabras de 32 bits)
            j: counter (64 bits)
            n: Nonce (64 bits)

        Returns:
            512 bits (16 palabras 32 bits)
        """

        s = split_words(s, 32 // 8, 8)
        j = split_words(j, 32 // 8, 2)
        n = split_words(n, 32 // 8, 2)

        return [
            self.c[0], s[0], s[1], s[2],
            s[3], self.c[1], n[0], n[1],
            j[0], j[1], self.c[2], s[4],
            s[5], s[6], s[7], self.c[3]
        ]

    
    def rot(self, w: int, r: int) -> int: 
        """No me acuerdo que hace esto 

        Args:
            w: Palabra a rotar
            r: No me acuerdo que es esto
        """

        mask = 0xffffffff
        return ((w << r) & mask) | (w >> (32 - r)) 

    
    def QR(self, a: int, b: int, c: int, d: int) -> Tuple[int, int, int, int]: 
        """Cuarto de ronda. Esta función es invertible.

        Args:
            a (int): palabra
            b (int): palabra
            c (int): palabra
            d (int): palabra

        Returns:
            Tuple[int, int, int, int]: secuencia de 4 palabras
        """
        b = b ^ self.rot(sum32(a, d), 7)
        c = c ^ self.rot(sum32(b, a), 9)
        d = d ^ self.rot(sum32(c, b), 13)
        a = a ^ self.rot(sum32(d, c), 18)
        
        return a, b, c, d

    
    def round(self, i: List[int]):  
        i[0], i[4], i[8], i[12] = self.QR(i[0], i[4], i[8], i[12]) 
        i[5], i[9], i[13], i[1] = self.QR(i[5], i[9], i[13], i[1]) 
        i[10], i[14], i[2], i[6] = self.QR(i[10], i[14], i[2], i[6]) 
        i[15], i[3], i[7], i[11] = self.QR(i[15], i[3], i[7], i[11]) 

        i[0], i[1], i[2], i[3] = self.QR(i[0], i[1], i[2], i[3]) 
        i[5], i[6], i[7], i[4] = self.QR(i[5], i[6], i[7], i[4]) 
        i[10], i[11], i[8], i[9] = self.QR(i[10], i[11], i[8], i[9])
        i[15], i[12], i[13], i[14] = self.QR(i[15], i[12], i[13], i[14])

        return i

    
    def perm(self, x: int, ROUNDS: int = 20): 
        """¨Permutación 

        Args:
            x: 512 bits (16 palabras de  32 bits)
            ROUNDS: Número de rondas
                - 20 (salsa20/20)
                - 8 (salsa20/8)
                - 12 (salsa20/12)
                
        Returns:
            512 bits (16 palabras de 32 bits)
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
                r[j] = join_words(pi, 32 // 8) + join_words(h, 32 // 8)
            
        return r
    
    
    def encrypt(self, k, n, m): 
        keys = self.G(k, n)
        return m ^ keys[0]

    
    def decrypt(self, k, n, c):
        keys = self.G(k, n)
        return c ^ keys[0]


if __name__ == '__main__':
    salsa = Salsa()

    assert(
        salsa.pad(
            0x112233445566778899aabbccddeeff00,
            0x0123456789abcdef,
            0xfedcba9876543210) == 
        
        [0x61707865, 0x0, 0x0, 0x0, 
         0x0, 0x3320646e, 0xfedcba98, 0x76543210,
         0x1234567, 0x89abcdef, 0x79622d32, 0x11223344,
         0x55667788, 0x99aabbcc, 0xddeeff00, 0x6b206574]
    ), "Pad test 1 failed"

    assert(
        salsa.pad(0x47f515b1dd45f8d5aceea73b52971be21f7b4b3355a35fd6a2799898ed2f8c97,
        0x722d9d570ac23201,
        0xed539cd99e1d2f20) ==
        
        [0x61707865, 0x47f515b1, 0xdd45f8d5, 0xaceea73b,
        0x52971be2, 0x3320646e,  0xed539cd9, 0x9e1d2f20,
        0x722d9d57, 0x0ac23201, 0x79622d32, 0x1f7b4b33,
        0x55a35fd6, 0xa2799898, 0xed2f8c97, 0x6b206574]
    ), "Pad test 2 failed"


    assert(salsa.QR(0x00000000, 0x00000000, 0x00000000, 0x00000000)
    == (0x00000000, 0x00000000, 0x00000000, 0x00000000)), "QR test 1 failed"
    assert(salsa.QR(0x00000001, 0x00000000, 0x00000000, 0x00000000)
    == (0x08008145, 0x00000080, 0x00010200, 0x20500000)), "QR test 2 failed"
    assert(salsa.QR(0x00000000, 0x00000001, 0x00000000, 0x00000000)
    == (0x88000100, 0x00000001, 0x00000200, 0x00402000)), "QR test 3 failed"
    assert(salsa.QR(0x00000000, 0x00000000, 0x00000001, 0x00000000)
    == (0x80040000, 0x00000000, 0x00000001, 0x00002000)), "QR test 4 failed"
    assert(salsa.QR(0x00000000, 0x00000000, 0x00000000, 0x00000001)
    == (0x00048044, 0x00000080, 0x00010000, 0x20100001)), "QR test 5 failed"
    assert(salsa.QR(0xe7e8c006, 0xc4f9417d, 0x6479b4b2, 0x68c67137)
    == (0xe876d72b, 0x9361dfd5, 0xf1460244, 0x948541a3)), "QR test 6 failed"
    assert(salsa.QR(0xd3917c5b, 0x55f1c407, 0x52a58a7a, 0x8f887a3b)
    == (0x3e2f308c, 0xd90a8f36, 0x6ab2a923, 0x2883524c)), "QR test 7 failed"

    assert(
        salsa.QR(0xc2619378, 0xecdaec96, 0xe62bd0c8, 0x2b61be56) ==
        (0x21158c0a, 0x0d720be0, 0x41156157, 0xc6c75786)
    ), "QR test 8 failed"

    assert(salsa.round([0x00000001, 0x00000000, 0x00000000, 0x00000000,
    0x00000000, 0x00000000, 0x00000000, 0x00000000,
    0x00000000, 0x00000000, 0x00000000, 0x00000000,
    0x00000000, 0x00000000, 0x00000000, 0x00000000]) == [0x8186a22d, 0x0040a284, 0x82479210, 0x06929051,
    0x08000090, 0x02402200, 0x00004000, 0x00800000,
    0x00010200, 0x20400000, 0x08008104, 0x00000000,
    0x20500000, 0xa0000040, 0x0008180a, 0x612a8020]), "Round test 1 failed"

    assert(salsa.round([0xde501066, 0x6f9eb8f7, 0xe4fbbd9b, 0x454e3f57,
    0xb75540d3, 0x43e93a4c, 0x3a6f2aa0, 0x726d6b36,
    0x9243f484, 0x9145d1e8, 0x4fa9d247, 0xdc8dee11,
    0x054bf545, 0x254dd653, 0xd9421b6d, 0x67b276c1]) == [0xccaaf672, 0x23d960f7, 0x9153e63a, 0xcd9a60d0,
    0x50440492, 0xf07cad19, 0xae344aa0, 0xdf4cfdfc,
    0xca531c29, 0x8e7943db, 0xac1680cd, 0xd503ca00,
    0xa74b2ad6, 0xbc331c5c, 0x1dda24c7, 0xee928277]), "Round test 2 failed"

    s = 0x47f515b1dd45f8d5aceea73b52971be21f7b4b3355a35fd6a2799898ed2f8c97
    j = 0x722d9d570ac23201
    n = 0xed539cd99e1d2f20

    _pad = salsa.pad(s, j, n)

    assert(join_words(salsa.perm(_pad), 32 // 8) == 0x4ae1c9a7e960b635dc60a70e05f3a06b6d5333b853e0b60d7fe901e08289149820c71b7f7bf63cd69222987510bb60608551ec51c1e23b31da929437ccb2cb58),"Perm test failed"

    s = 0x112233445566778899aabbccddeeff00
    n = 0x0123456789abcdef
    m = text_to_int("Hola mundo!")
    assert(salsa.decrypt(s, n, salsa.encrypt(s, n, m)) == m), "Error"