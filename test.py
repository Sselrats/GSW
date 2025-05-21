from utils import *
from gsw import GSW

import numpy as np
from collections import Counter

n = 5
logq = 10
q = 2**logq

test_num = 256

def GSW_correction_test():
    print(f"=== GSW_correction_test ===")
    good = 0
    bad = 0
    broken = 0
    for _ in range(test_num):
        gsw = GSW(n, q)
        msg = uniform_sample([0, 1])
        ctxt = gsw.Enc(msg)
        s_ = gsw.generate_s()

        if (msg == gsw.Dec_with_key(ctxt, s_)):
            good += 1
        else:
            bad += 1
        
        if (msg != gsw.Dec(ctxt)):
            broken += 1

    print("Properly decrypted with random key: ", good)
    print("Failed to decrypt with random key: ", bad)
    
    if broken == 0:
        print("Test passed!")
    else:
        print("Test failed with broken:", broken)


def G_inverse_test():
    print(f"=== G_inverse_test ===")
    broken = 0
    for _ in range(test_num):
        gsw = GSW(n, q)
        M = np.random.randint(0, q, (gsw.l, gsw.n+1))
        G_inv_M = gsw.generate_G_inverse(M)

        if not check_modq(G_inv_M @ gsw.G, M, q):
            broken += 1

    if broken == 0:
        print("Test passed!")
    else:
        print("Test failed with broken:", broken)

def GSW_Ciphertext_Error_test():
    print(f"=== GSW_Ciphertext_Error_test ===")
    broken = 0
    for _ in range(test_num):
        gsw = GSW(n, q)
        msg = uniform_sample([0, 1])
        ctxt = gsw.Enc(msg)

        if ctxt.get_error(msg) not in [0, 1]:
            broken += 1

    if broken == 0:
        print("Test passed!")
    else:
        print("Test failed with broken:", broken)

def GSW_Ciphertext_Add_test():
    print(f"=== GSW_Ciphertext_Add_test ===")
    broken = 0
    for _ in range(test_num):
        gsw = GSW(n, q)
        msg1 = uniform_sample([0, 1])
        msg2 = uniform_sample([0, 1])
        ctxt1 = gsw.Enc(msg1)
        ctxt2 = gsw.Enc(msg2)

        ctxt1.Add(ctxt2)

        if (msg1 + msg2) % 2 != gsw.Dec(ctxt1):
            broken += 1

    if broken == 0:
        print("Test passed!")
    else:
        print("Test failed with broken:", broken)


def GSW_Ciphertext_Mult_test():
    print(f"=== GSW_Ciphertext_Mult_test ===")
    broken = 0
    for _ in range(test_num):
        gsw = GSW(n, q)
        msg1 = uniform_sample([0, 1])
        msg2 = uniform_sample([0, 1])
        ctxt1 = gsw.Enc(msg1)
        ctxt2 = gsw.Enc(msg2)
        ctxt1.Mult(ctxt2)

        if msg1 * msg2 != gsw.Dec(ctxt1):
            broken += 1

    if broken == 0:
        print("Test passed!")
    else:
        print("Test failed with broken:", broken)

def GSW_Ciphertext_Error_On_Single_Add_test():
    print(f"=== GSW_Ciphertext_Error_On_Single_Add_test ===")
    broken = 0
    errors = []
    for _ in range(test_num):
        gsw = GSW(n, q)
        msg1 = uniform_sample([0, 1])
        msg2 = uniform_sample([0, 1])
        ctxt1 = gsw.Enc(msg1)
        ctxt2 = gsw.Enc(msg2)

        ctxt1.Add(ctxt2)

        error12 = ctxt1.get_error((msg1 + msg2) % 2)
        errors.append(error12)

        if error12 not in [0, 1, 2]:
            broken += 1

    print("Errors:", [Counter(errors)[i] for i in [0, 1, 2]])

    if broken == 0:
        print("Test passed!")
    else:
        print("Test failed with broken:", broken)
    

def run_tests():
    GSW_correction_test()
    G_inverse_test()
    GSW_Ciphertext_Error_test()
    GSW_Ciphertext_Add_test()
    GSW_Ciphertext_Mult_test()
    GSW_Ciphertext_Error_On_Single_Add_test()

if __name__ == "__main__":
    run_tests()
