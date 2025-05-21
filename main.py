from gsw import GSW


def main():
    n = 5
    logq = 10
    q = 2**logq
    gsw = GSW(n, q)
    
    message = 1
    ciphertext = gsw.Enc(message)
    decrypted = gsw.Dec(ciphertext)
    
    print(f"Original message: {message}")
    print(f"Decrypted message: {decrypted}")


if __name__ == "__main__":
    main()
