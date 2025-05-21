import numpy as np

n = 5
logq = 10
q = 2**logq
l = (n + 1) * logq
Z_q = range(q)

def uniform_sample(space):
    return np.random.choice(space)

def check_modq(A, B):
    return np.array_equal(A % q, B % q)

def get_error():
    e = np.ones((l, 1), dtype=np.int32)
    for i in range(l):
        e[i] = uniform_sample([0, 1])

    return e

def generate_s(n = n):
    s = np.ones((n+1, 1), dtype=np.int32)
    for i in range(1, n+1):
        s[i] = uniform_sample([0, 1])

    return s

def encode(msg):
    return msg * q // 2

def generate_G():
    G = np.zeros((l, n+1), dtype=np.int32)
    for i in range(l):
        G[i][i // logq] = 2**(i%logq)

    return G

def Enc(s, msg):
    e = get_error()
    Cs = encode(msg) * (G @ s) + e

    C_ = np.ones((l, n), dtype=np.int32)
    for i in range(l):
        for j in range(n):
            C_[i][j] = uniform_sample(Z_q)

    s_ = s[1:]

    C = np.concatenate((-C_ @ s_ + Cs, C_), axis=1) % q
    return C

def Dec(s, C):
    c0 = C[0]
    encoded = (c0 @ s)[0] % q
    ptxt = encoded * 2 // q
    return ptxt

test_num = 1000
msgs = [uniform_sample([0, 1]) for _ in range(test_num)]
good = 0
bad = 0

for msg in msgs:
    s = generate_s()
    G = generate_G()
    ctxt = Enc(s, msg)

    s_ = generate_s()
    ptxt = Dec(s_, ctxt)
    if (msg == ptxt):
        good += 1
    else:
        bad += 1

print("Good: ", good)
print("Bad: ", bad)

s = generate_s()

msg1 = 1
msg2 = 1

ctxt1 = Enc(s, msg1)
ctxt2 = Enc(s, msg2)
