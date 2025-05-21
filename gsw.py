from utils import uniform_sample
import numpy as np

class GSW:
    def __init__(self, n, q):
        self.n = n
        self.q = q
        self.logq = int(np.log2(q))
        self.l = (n + 1) * self.logq
        self.Z_q = range(q)

        self.s = self.generate_s()

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
        return msg * self.q // 2

    def generate_G(self):
        G = np.zeros((self.l, self.n+1), dtype=np.int32)
        for i in range(self.l):
            G[i][i // self.logq] = 2**(i%self.logq)

        return G

    def Enc(self, msg):
        e = self.get_error()
        Cs = self.encode(msg) * (self.generate_G() @ self.s) + e

        C_ = np.ones((self.l, self.n), dtype=np.int32)
        for i in range(self.l):
            for j in range(self.n):
                C_[i][j] = uniform_sample(self.Z_q)

        s_ = self.s[1:]

        C = np.concatenate((-C_ @ s_ + Cs, C_), axis=1) % self.q
        return C

    def Dec_with_key(self, C, s):
        c0 = C[0]
        encoded = (c0 @ s)[0] % self.q
        ptxt = encoded * 2 // self.q
        return ptxt

    def Dec(self, C):
        return self.Dec_with_key(C, self.s)
