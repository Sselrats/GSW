from utils import *
from gsw import GSW

n = 5
logq = 10
q = 2**logq

def run_tests():
    gsw = GSW(n, q)

    test_num = 1000
    msgs = [uniform_sample([0, 1]) for _ in range(test_num)]
    good = 0
    bad = 0
    broken = 0

    for msg in msgs:
        ctxt = gsw.Enc(msg)
        s_ = gsw.generate_s()

        if (msg == gsw.Dec_with_key(ctxt, s_)):
            good += 1
        else:
            bad += 1
        
        if (msg != gsw.Dec(ctxt)):
            broken += 1

    print("Good: ", good)
    print("Bad: ", bad)
    print("Broken: ", broken)


if __name__ == "__main__":
    run_tests()
