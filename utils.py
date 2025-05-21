import numpy as np

def uniform_sample(space):
    return np.random.choice(space)


def check_modq(A, B, q):
    return np.array_equal(A % q, B % q)
