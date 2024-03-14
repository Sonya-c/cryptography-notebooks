
from typing import List
from utils import split_words, join_words, text_to_int, f28_mult, to_matrix

class AES:

    s_box: List[int] = [
        0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
        0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
        0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
        0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
        0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
        0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
        0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
        0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
        0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
        0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
        0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
        0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
        0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
        0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
        0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
        0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16
    ]

    s_box_inv: List[int] = [
        0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
        0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
        0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
        0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
        0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
        0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
        0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
        0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
        0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
        0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
        0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
        0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
        0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
        0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
        0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
        0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D
    ]

    M: List[List[int]]= [
        [0x02, 0x03, 0x01, 0x01],
        [0x01, 0x02, 0x03, 0x01],
        [0x01, 0x01, 0x02, 0x03],
        [0x03, 0x01, 0x01, 0x02],
    ]

    M_inv: List[List[int]] = [
        [0x0e, 0x0b, 0x0d, 0x09],
        [0x09, 0x0e, 0x0b, 0x0d],
        [0x0d, 0x09, 0x0e, 0x0b],
        [0x0b, 0x0d, 0x09, 0x0e],
    ]

    RC = [
        0b00000001,
        0b00000010,
        0b00000100,
        0b00001000,
        0b00010000,
        0b00100000,
        0b01000000,
        0b10000000,
        0b00011011,
        0b00110110
    ]

    def byte_sub(self, state: List[List[int]]) -> List[List[int]]: 
        return [ [self.s_box[x] for x in row] for row in state ] 

    def byte_sub_inv(self, state: List[List[int]]) -> List[List[int]]: 
        return [[self.s_box_inv[x] for x in row] for row in state]  

    def shift(self, seq: List[any], n: int) -> List[any]:
        n = n % len(seq)
        return seq[n:] + seq[:n]

    def shift_rows(self, B: List[List[int]]) -> List[List[int]]: 
        return [
            self.shift(B[0], 0),
            self.shift(B[1], 1),
            self.shift(B[2], 2),
            self.shift(B[3], 3),
        ]

    def shift_rows_inv(self, B: List[List[int]]) -> List[List[int]]: 
        return [
            self.shift(B[0], 0),
            self.shift(B[1], -1),
            self.shift(B[2], -2),
            self.shift(B[3], -3),
        ]

    def mix_collumns(self, state: List[List[int]]) -> List[List[int]]: 
        C: List[List[int]]= [[0 for _ in range(4)] for _ in range(4)]
        
        for i in range(4):
            for j in range(4):
                C[i][j] = (
                    f28_mult(self.M[i][0], state[0][j]) ^
                    f28_mult(self.M[i][1], state[1][j]) ^
                    f28_mult(self.M[i][2], state[2][j]) ^
                    f28_mult(self.M[i][3], state[3][j])
                ) & 0xFF 
        
        return C

    def mix_collumns_inv(self, state: List[List[int]]) -> List[List[int]]: 
        C: List[List[int]]= [[0 for _ in range(4)] for _ in range(4)]
        
        for i in range(4):
            for j in range(4):
                C[i][j] = (
                    f28_mult(self.M_inv[i][0], state[0][j]) ^
                    f28_mult(self.M_inv[i][1], state[1][j]) ^
                    f28_mult(self.M_inv[i][2], state[2][j]) ^
                    f28_mult(self.M_inv[i][3], state[3][j])
                ) & 0xFF 
        
        return C

    def key_addition(self, state: List[List[int]], k: List[List[int]]) -> List[List[int]]: 

        assert(len(state) == len(k)), "State and k must have same size"
        
        _state = state.copy()

        for row1, row2 in zip(_state, k):
            assert(len(row1) == len(row2)), "Rows must have same size"

            for i in range(len(row1)):
                row1[i] ^= row2[i]
        
        return _state
    
    def g(self, w: int, i: int) -> int: 
        """
        Args:
            w (int): 16 bit palabra
            i (int): número de ronda
            
        Returns:
            int: 16 bit palabra
        """

        v = split_words(w, 1, 4)

        v = [v[1], v[2], v[3], v[0]]
        
        # byte subtituion 
        v = [self.s_box[vi] for vi in v]

        
        # XOR
        v[0] ^= self.RC[i]
        
        return join_words(v, 1)

    def h(self, w: int) -> int: 
        """h

        Args:
            w (int): palabra 16 bit
            i (int): numero de roneda

        Returns:
            int: palabra 16 bit
        """

        v = split_words(w, 1, 4)
        
        # byte subtituion 
        v = [self.s_box[vi] for vi in v]
        
        return join_words(v, 1)

    def expansion_key128(self, k: List[int]):   
        assert(len(k) == 4)
        
        w = [0]*(44)

        w[0] = k[0]
        w[1] = k[1]
        w[2] = k[2]
        w[3] = k[3]
        
        for i in range(1, 10 + 1):
            w[4*i] = w[4 * (i - 1)] ^ self.g(w[4 * i - 1], i - 1)
            w[4*i + 1] = w[4 * (i - 1) + 1] ^ w[4 * i]
            w[4*i + 2] = w[4 * (i - 1) + 2] ^ w[4 * i + 1]
            w[4*i + 3] = w[4 * (i - 1) + 3] ^ w[4 * i + 2] 
            
        return w

    def expansion_key192(self, k: List[int]):   
        w = [0]* 52

        w[0] = k[0]
        w[1] = k[1]
        w[2] = k[2]
        w[3] = k[3]
        w[4] = k[4]
        w[5] = k[5]

        for i in range(1, 8 + 1):    
            w[6*i] = w[6 * (i - 1)] ^ self.g(w[6 * i - 1], i - 1)
            w[6*i + 1] = w[6 * (i - 1) + 1] ^ w[6 * i]
            w[6*i + 2] = w[6 * (i - 1) + 2] ^ w[6 * i + 1]
            w[6*i + 3] = w[6 * (i - 1) + 3] ^ w[6 * i + 2]

            if (i == 8): break # pass last two

            w[6*i + 4] = w[6 * (i - 1) + 4] ^ w[6 * i + 3]
            w[6*i + 5] = w[6 * (i - 1) + 5] ^ w[6 * i + 4]

        return w

    def expansion_key256(self, k: List[int]):   
        w = [0]* 60

        w[0] = k[0]
        w[1] = k[1]
        w[2] = k[2]
        w[3] = k[3]
        w[4] = k[4]
        w[5] = k[5]
        w[6] = k[6]
        w[7] = k[7]

        for i in range(1, 7 + 1):    
            w[8*i] = w[8 * (i - 1)] ^ self.g(w[8 * i - 1], i - 1)
            w[8*i + 1] = w[8 * (i - 1) + 1] ^ w[8 * i]
            w[8*i + 2] = w[8 * (i - 1) + 2] ^ w[8 * i + 1]
            w[8*i + 3] = w[8 * (i - 1) + 3] ^ w[8 * i + 2]

            if (i == 7): break # skip last two

            w[8*i + 4] = w[8 * (i - 1) + 4] ^ self.h(w[8 * i + 3])
            w[8*i + 5] = w[8 * (i - 1) + 5] ^ w[8 * i + 4]
            w[8*i + 6] = w[8 * (i - 1) + 6] ^ w[8 * i + 5]
            w[8*i + 7] = w[8 * (i - 1) + 7] ^ w[8 * i + 6]

        return w

    def encrypt(self, m: int, k: int):
        assert(len(bin(k)) <= 256), "Key must be 256 bits or less"

        if (len(bin(k)) <= 128):
            w = self.expansion_key128(split_words(k, 4, 4))
            rounds = 10
        elif (len(bin(k)) <= 192):
            w = self.expansion_key192(split_words(k, 4, 6))
            rounds = 12
        else:
            w = self.expansion_key256(split_words(k, 4, 8))
            rounds = 14

        keys = [join_words(w[i:i+4], 4) for i in range(0, len(w), 4)]
        
        A = to_matrix(m)
        k = to_matrix(keys[0])
        A = self.key_addition(A, k)

        for i in range(1, rounds + 1):
            # A es la matrix de entrada de la ronda i
            # if (i == 1): print(hex(join_words([A[i][j] for j in range(4) for i in range(4)], 1)))

            # B es la matriz resultante de ejecutar byte_sub
            B = self.byte_sub(A)
            # if (i == 12): print(hex(join_words([B[i][j] for j in range(4) for i in range(4)], 1)))
            
            # Bs Es la matriz resultante de ejecutar shitrows
            Bs = self.shift_rows(B)
            # if (i == 5): print_hex_matrix(Bs)

            # C es la matrix resultante de ejecutar mix collums 
            C = self.mix_collumns(Bs) if (i != rounds) else Bs         

            k = to_matrix(keys[i])
            A = self.key_addition(C, k)
        
        return join_words([A[i][j] for j in range(4) for i in range(4)], 1)

    def decrypt(self, c, k):
        assert(len(bin(k)) <= 256), "Key must be 256 bits or less"

        if (len(bin(k)) <= 128):
            w = self.expansion_key128(split_words(k, 4, 4))
            rounds = 10
        elif (len(bin(k)) <= 192):
            w = self.expansion_key192(split_words(k, 4, 6))
            rounds = 12
        else:
            w = self.expansion_key256(split_words(k, 4, 8))
            rounds = 14

        keys = [join_words(w[i:i+4], 4) for i in range(0, len(w), 4)]
        
        A = to_matrix(c)

        for i in range(rounds, 0, -1):
            k = to_matrix(keys[i])
            C = self.key_addition(A, k)

            
            Bs = self.mix_collumns_inv(C) if (i != rounds) else C        

            B = self.shift_rows_inv(Bs)
            A = self.byte_sub_inv(B)
        
        
        k = to_matrix(keys[0])
        A = self.key_addition(A, k)
        return join_words([A[i][j] for j in range(4) for i in range(4)], 1)

    

if __name__ == '__main__':
    aes = AES()

    assert(aes.byte_sub([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]]) == [[124, 119, 123, 242], [107, 111, 197, 48], [1, 103, 43, 254], [215, 171, 118, 202]]), "Byte sub failed"

    assert(aes.byte_sub_inv([[124, 119, 123, 242], [107, 111, 197, 48], [1, 103, 43, 254], [215, 171, 118, 202]]) == [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]), "Byte inv failed"

    assert(aes.shift_rows([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]) == [[1, 2, 3, 4], [6, 7, 8, 5], [11, 12, 9, 10], [16, 13, 14, 15]]), "Shift rows failed"

    assert(aes.shift_rows_inv([[1, 2, 3, 4], [6, 7, 8, 5], [11, 12, 9, 10], [16, 13, 14, 15]]) == [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]), "Shift rows inv failed"

    assert(aes.mix_collumns([
        [0x33, 0x3b, 0x61, 0x50],
        [0x1c, 0x4f, 0xea, 0xaf],
        [0x38, 0xb7, 0x21, 0xa9],
        [0xc9, 0x4d, 0x44, 0x2d]
    ]) == [
        [0xb3, 0x5d, 0x82, 0xce],
        [0x8a, 0x2a, 0x89, 0xd8],
        [0x1f, 0xd6, 0x5,  0xc1],
        [0xf8, 0x2f, 0xe0, 0xac],
    ]), "Failed mix collumns"

    assert(aes.mix_collumns_inv([
        [0xb3, 0x5d, 0x82, 0xce],
        [0x8a, 0x2a, 0x89, 0xd8],
        [0x1f, 0xd6, 0x5,  0xc1],
        [0xf8, 0x2f, 0xe0, 0xac],
    ]) == [
        [0x33, 0x3b, 0x61, 0x50],
        [0x1c, 0x4f, 0xea, 0xaf],
        [0x38, 0xb7, 0x21, 0xa9],
        [0xc9, 0x4d, 0x44, 0x2d]
    ]), "Failed mix collums inv"

    assert(aes.key_addition([
        [0x4d, 0x61, 0x73, 0x65],
        [0x65, 0x6a, 0x65, 0x74],
        [0x6e, 0x65, 0x63, 0x6f],
        [0x73, 0x20, 0x72, 0x2e],
    ], [
        [0x2b, 0x28, 0xab, 0x9],
        [0x7e, 0xae, 0xf7, 0xcf],
        [0x15, 0xd2, 0x15, 0x4f],
        [0x16, 0xa6, 0x88, 0x3c]
    ]) == [
        [0x66, 0x49, 0xd8, 0x6c],
        [0x1b, 0xc4, 0x92, 0xbb],
        [0x7b, 0xb7, 0x76, 0x20],
        [0x65, 0x86, 0xfa, 0x12],
    ]), "AES key addition failed"


    assert(aes.g(0x1A38B5EE, 5) == 0x27d528A2), "G test 1 failed"
    assert(aes.g(0x09CF4F3C, 0) == 0x8B84EB01), "G test 2 failed"

    k0 = split_words(0x2b7e151628aed2a6abf7158809cf4f3c, 4, 4)
    w = aes.expansion_key128(k0)
    rks = [join_words(w[i:i+4], 4) for i in range(0, len(w), 4)]

    assert(rks[1] == 0xa0fafe1788542cb123a339392a6c7605), "Key128 1 is wrong"
    assert(rks[2] == 0xf2c295f27a96b9435935807a7359f67f), "Key128 2 is wrong"
    assert(rks[3] == 0x3d80477d4716fe3e1e237e446d7a883b), "Key128 3 is wrong"
    assert(rks[4] == 0xef44a541a8525b7fb671253bdb0bad00), "Key128 4 is wrong"
    assert(rks[5] == 0xd4d1c6f87c839d87caf2b8bc11f915bc), "Key128 5 is wrong"
    assert(rks[6] == 0x6d88a37a110b3efddbf98641ca0093fd), "Key128 6 is wrong"
    assert(rks[7] == 0x4e54f70e5f5fc9f384a64fb24ea6dc4f), "Key128 7 is wrong"
    assert(rks[8] == 0xead27321b58dbad2312bf5607f8d292f), "Key128 8 is wrong"
    assert(rks[9] == 0xac7766f319fadc2128d12941575c006e), "Key128 9 is wrong"
    assert(rks[10] ==0xd014f9a8c9ee2589e13f0cc8b6630ca6), "Key128 10 is wrong"

    k = split_words(0x8e73b0f7da0e6452c810f32b809079e562f8ead2522c6b7b, 4, 6)
    w = aes.expansion_key192(k)
    rks = [join_words(w[i:i+6], 4) for i in range(0, len(w), 6)]


    assert(rks[1] == 0xfe0c91f72402f5a5ec12068e6c827f6b0e7a95b95c56fec2), "Key 1 is wrong"
    assert(rks[2] == 0x4db7b4bd69b5411885a74796e92538fde75fad44bb095386), "Key 2 is wrong"
    assert(rks[3] == 0x485af05721efb14fa448f6d94d6dce24aa326360113b30e6), "Key 3 is wrong"
    assert(rks[4] == 0xa25e7ed583b1cf9a27f939436a94f767c0a69407d19da4e1), "Key 4 is wrong"
    assert(rks[5] == 0xec1786eb6fa64971485f703222cb8755e26d135233f0b7b3), "Key 5 is wrong"
    assert(rks[6] == 0x40beeb282f18a2596747d26b458c553ea7e1466c9411f1df), "Key 6 is wrong"
    assert(rks[7] == 0x821f750aad07d753ca4005388fcc5006282d166abc3ce7b5), "Key 7 is wrong"
    assert(rks[8] == 0xe98ba06f448c773c8ecc720401002202), "Key 8 is wrong"

    k = split_words(0x603deb1015ca71be2b73aef0857d77811f352c073b6108d72d9810a30914dff4, 4, 8)
    w = aes.expansion_key256(k)
    rks = [join_words(w[i:i+8], 4) for i in range(0, len(w), 8)]

    assert(rks[1] == 0x9ba354118e6925afa51a8b5f2067fcdea8b09c1a93d194cdbe49846eb75d5b9a), "Key 1 is wrong"
    assert(rks[2] == 0xd59aecb85bf3c917fee94248de8ebe96b5a9328a2678a647983122292f6c79b3), "Key 2 is wrong"
    assert(rks[3] == 0x812c81addadf48ba24360af2fab8b46498c5bfc9bebd198e268c3ba709e04214), "Key 3 is wrong"
    assert(rks[4] == 0x68007bacb2df331696e939e46c518d80c814e20476a9fb8a5025c02d59c58239), "Key 4 is wrong"
    assert(rks[5] == 0xde1369676ccc5a71fa2563959674ee155886ca5d2e2f31d77e0af1fa27cf73c3), "Key 5 is wrong"
    assert(rks[6] == 0x749c47ab18501ddae2757e4f7401905acafaaae3e4d59b349adf6acebd10190d), "Key 6 is wrong"
    assert(rks[7] == 0xfe4890d1e6188d0b046df344706c631e), "Key 7 is wrong"

    assert(aes.encrypt(0x3243f6a8885a308d313198a2e0370734, 0x2b7e151628aed2a6abf7158809cf4f3c) == 0x3925841d02dc09fbdc118597196a0b32)

    # Test parcial 1

    assert(aes.encrypt(0x4fc86c3764d13f5dbe2e89090fc49581,0x1c433e7115843eab4a20d445cbe647680881cb077fc50372c2d754ae6106dd8f) == 0xaf7753d9a795a586be3a7ce954806e03), "M1 failed"
    assert(aes.encrypt(0x173c0b3879620ef70731c55eb4f26a2a,0x1c433e7115843eab4a20d445cbe647680881cb077fc50372c2d754ae6106dd8f) == 0x8502e9f8a080cd7f0d57f157cf82ccb5), "M2 failed"
    assert(aes.encrypt(0x9a022558563774b7f461cfb72f196d78,0x1c433e7115843eab4a20d445cbe647680881cb077fc50372c2d754ae6106dd8f) == 0x71feb16568cf370d872bd1f3396116ff), "M3 failed"
    assert(aes.encrypt(0xb26e04d63ce379ee94a46b888af7c2ee,0x1c433e7115843eab4a20d445cbe647680881cb077fc50372c2d754ae6106dd8f) == 0x3733e17a34737dcf5968d65a11d4e404), "M4 failed"
    assert(aes.encrypt(0x75af92cebbe06eb63b0b2bc2d0d86864,0x1c433e7115843eab4a20d445cbe647680881cb077fc50372c2d754ae6106dd8f) == 0xaed847d964f82d18e5e70c347610402d), "M5 failed"

    assert(aes.decrypt(0x3925841d02dc09fbdc118597196a0b32, 0x2b7e151628aed2a6abf7158809cf4f3c) == 0x3243f6a8885a308d313198a2e0370734)
