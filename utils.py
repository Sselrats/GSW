import numpy as np

def uniform_sample(space):
    return np.random.choice(space)

def check_modq(A, B, q):
    return np.array_equal(A % q, B % q)

def decompose(n, logq):
    return [(n >> i) & 1 for i in range(logq)]
