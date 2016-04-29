import Crypto.Util.number as pycrypto

PRIME_SIZE = 1024

def gen_keys():
    p = pycrypto.getPrime(PRIME_SIZE)
    q = pycrypto.getPrime(PRIME_SIZE)
    n = p * q
    l = ((p-1) * (q-1))//pycrypto.GCD(p-1,q-1)
    while True:
        g = pycrypto.getRandomInteger(PRIME_SIZE * 4) % (n * n)
        if pycrypto.GCD(g,n) == 1:
            c = (pow(g, l, n * n) - 1)//n
            if pycrypto.GCD(c, n) == 1:
                mu = pycrypto.inverse(c, n)
                break

    return PublicKey(n,g), PrivateKey(l, mu)

def encrypt(pk, msg):
    while True:
        r = pycrypto.getRandomInteger(PRIME_SIZE * 2)
        if pycrypto.GCD(r,pk.n) == 1:
            break
    return ((pow(pk.g, msg, pk.n * pk.n) * pow(r, pk.n, pk.n * pk.n)) % (pk.n * pk.n), r)

def decrypt(pk, sk, c):
    u = pow(c, sk.l, pk.n * pk.n)
    L = (u - 1)//pk.n
    return (L * sk.mu) % pk.n

def add(pk, c1, c2):
    return (c1 * c2) % (pk.n * pk.n)

class PublicKey:
    def __init__(self, n, g):
        self.n = n
        self.g = g

class PrivateKey:
    def __init__(self, l, mu):
        self.l = l
        self.mu = mu

if __name__ == '__main__':
    pk, sk = gen_keys()
    c1 = encrypt(pk, 1)
    c2 = encrypt(pk, 2)
    c = add(pk, c1, c2)
    print(decrypt(pk, sk, c))
