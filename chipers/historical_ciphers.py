import random 

alphabeth = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']


class CesarCipher: 
    def __init__(self, k: int, alphabeth = alphabeth) -> None: 
        self.alphabeth = alphabeth
        self.k = k % len(alphabeth) 

    def encrypt(self, m) -> str:
        c = ''

        for m_i in m: 
            r_i = self.alphabeth.index(m_i)
            c += self.alphabeth[(r_i + self.k) % len(self.alphabeth)]
        return c

    def decrypt(self, c) -> str:
        m = ''
        for c_i in c: 
            r_i = self.alphabeth.index(c_i)
            m += self.alphabeth[(r_i - self.k) % len(self.alphabeth)]
        return m
    


class SubstitutionCipher: 

    def __init__(self, alphabeth = alphabeth, perm_alphabeth = None) -> None: 
        if (perm_alphabeth == None):
            perm_alphabeth = alphabeth.copy()
            random.shuffle(perm_alphabeth)
            print("Random permutation = ", perm_alphabeth)

        self.perm = dict(zip(alphabeth, perm_alphabeth))

    def encrypt(self, m) -> None:
        c = ''
        for m_i in m:
            c += self.perm[m_i]
        return c
        
    def decrypt(self, c):
        m = ''
        for c_i in c: 
            r_i = list(self.perm.values()).index(c_i)
            m += list(self.perm.keys())[r_i]
            
        return m
    
class OneTimePad: 

    def __init__(self, k) -> None: 
        self.k = k

    def encrypt(self, m) -> None: 
        return m ^ self.k

    def decrypt(self, c) -> None: 
        return c ^ self.k 