
from typing import List
import random 
from AES import AES


class ECB:

    def __init__(self, cipher) -> None:
        self.cipher = cipher

    def encrypt(self, m: int, k: int) -> List[int]:
        return [self.cipher.encrypt(mi, k) for mi in m]
    
    def decrypt(self, c: int, k: int):
        return [self.cipher.decrypt(ci, k) for ci in c]

class CBC:

    def __init__(self, cipher) -> None:
        self.cipher = cipher

    def encrypt(self, m: int, k: int) -> List[int]:
        iv = int.from_bytes(random.randbytes(len(bin(m[0])) // 8))
        c = [iv]
        # print("iv = ", iv)
        for i in range(len(m)):
            c.append(self.cipher.encrypt(m[i] ^ c[i], k))

        return c
    
    def decrypt(self, c: int, k: int):
        return [self.cipher.decrypt(c[i], k) ^ c[i - 1] for i in range(1, len(c))]

class Counter: 
    def __init__(self, cipher) -> None:
        self.cipher = cipher

    def encrypt(self, m: int, k: int, CI) -> List[int]:
        psudo_random = random.Random(CI)
        iv = int.from_bytes(psudo_random.randbytes(len(bin(m[0])) // 8))

        ctr = 0
        c = []
        for i in range(len(m)):
            c.append(self.cipher.encrypt(iv | ctr, k) ^ m[i])
            ctr = (ctr + 1) % (2 ** len(m))
        
        return c
    
    def decrypt(self, c: int, k: int, CI):
        psudo_random = random.Random(CI)
        iv = int.from_bytes(psudo_random.randbytes(len(bin(c[0])) // 8))

        ctr = 0
        m = []

        for i in range(len(c)):
            m.append(self.cipher.encrypt(iv | ctr, k) ^ c[i])
            ctr = (ctr + 1) % (2 ** len(c))
        
        return m
       
if __name__ == '__main__':
    aes = AES()

    ecb = ECB(aes)
    cbc = CBC(aes)
    counter = Counter(aes)

    k = 0x1c433e7115843eab4a20d445cbe647680881cb077fc50372c2d754ae6106dd8f
    0x1c433e7115843eab4a20d445cbe647680881cb077fc50372c2d754ae6106dd8f

    M = [0xe8468d5d7bd908d8ff599fbee3579609,
        0x257e68ddd87c93e143175740e896741f,
        0x5cff5ad4651042f5ecb3bdf10b129e5f,
        0x684aa62a4fc8c2af79e9a69402c78d12,
        0x63670680ac03d8bc19c2b554e2d10b22]

    assert(ecb.decrypt(ecb.encrypt(M, k), k) == M), "Failed ecb"
    assert(cbc.decrypt(cbc.encrypt(M, k), k) == M), "Failed cbc"

    CI = 3
    assert(counter.decrypt(counter.encrypt(M, k, CI), k, CI) == M), "Failed counter"


