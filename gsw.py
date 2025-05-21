from utils import decompose, uniform_sample
import numpy as np

class GSW:
    def __init__(self, n, q):
        self.n = n
        self.q = q
        self.logq = int(np.log2(q))
        self.l = (n + 1) * self.logq
        self.s = self.generate_s()
        self.G = self.generate_G()

    def get_error(self):
        e = np.ones((self.l, 1), dtype=np.int32)
        for i in range(self.l):
            e[i] = uniform_sample([0, 1])

        return e

    def generate_s(self):
        s = np.ones((self.n+1, 1), dtype=np.int32)
        for i in range(1, self.n+1):
            s[i] = uniform_sample([0, 1])

        return s

    def encode(self, msg):
        return msg * (self.q // 2)

    def decode(self, encoded):
        return np.round(encoded / (self.q // 2)).astype(np.int32)

    def generate_G(self):
        G = np.zeros((self.l, self.n+1), dtype=np.int32)
        for i in range(self.l):
            G[i][i // self.logq] = 2**(i % self.logq)

        return G
    
    # G_inv_M * G = M
    def generate_G_inverse(self, M):
        if (self.n+1 != M.shape[1]):
            raise ValueError("G and M must have the same number of columns")
        
        G_inv_M = np.zeros((M.shape[0], self.l), dtype=np.int32)
        for i in range(M.shape[0]):
            for j in range(self.l):
                G_inv_M[i][j] = decompose(M[i][j // self.logq], self.logq)[j % self.logq]

        return G_inv_M % self.q

    def Enc(self, msg):
        e = self.get_error()
        Cs = self.encode(msg) * (self.G @ self.s) + e

        C_ = np.ones((self.l, self.n), dtype=np.int32)
        for i in range(self.l):
            for j in range(self.n):
                C_[i][j] = uniform_sample(range(self.q))

        s_ = self.s[1:]
        C = np.concatenate((-C_ @ s_ + Cs, C_), axis=1) % self.q

        return GSW_Ciphertext(self, C)

    def Dec_with_key(self, ctxt, s):
        encoded = (ctxt.C[0] @ s)[0] % self.q

        return self.decode(encoded)

    def Dec(self, ctxt):
        return self.Dec_with_key(ctxt, self.s)

class GSW_Ciphertext:
    def __init__(self, gsw, C):
        self.gsw = gsw
        self.C = C

    def get_error(self, ptxt):
        G = self.gsw.G
        s = self.gsw.s

        error_vec = ((self.C @ s) - self.gsw.encode(ptxt) * (G @ s)) % self.gsw.q

        return abs(error_vec[0][0])
    
    def is_error_valid(self, ptxt):
        return self.get_error(ptxt) < self.gsw.q // 2

    def Dec_with_key(self, s):
        encoded = (self.C[0] @ s)[0] % self.gsw.q

        return self.gsw.decode(encoded)

    def Add(self, other):
        self.C = (self.C + other.C) % self.gsw.q

        return self

    def Mult(self, other):
        C = (self.gsw.generate_G_inverse(self.C) @ other.C) / (self.gsw.q // 2)
        self.C = np.round(C).astype(np.int32) % self.gsw.q

        return self