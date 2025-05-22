import numpy as np

def uniform_sample(space, n = 1):
    return np.random.choice(space, n)


def is_two_array_same_in_modq(A, B, q):
    return np.array_equal(A % q, B % q)

def decompose(n, logq):
    return [(n >> i) & 1 for i in range(logq)]
