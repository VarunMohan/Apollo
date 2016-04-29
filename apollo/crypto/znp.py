import Crypto.Util.number as pycrypto

PRIME_SIZE = 1024

def gen_proof(pk, u, esum, real, v):
    a = []
    z = []
    e = []
    n = pk.n
    r = None

    for i in range(len(u)):
        if i != real:
            newz = pycrypto.getRandomInteger(PRIME_SIZE*2)
            newe = pycrypto.getRandomInteger(PRIME_SIZE)
            newa = (pow(newz, n, n * n) * pycrypto.inverse(pow(u[i], newe, n * n), n * n)) % (n * n)
            z.append(newz)
            e.append(newe)
            a.append(newa)
        else:
            r = pycrypto.getRandomInteger(PRIME_SIZE*2)
            newa = pow(r, n, n * n)

            a.append(newa)
            z.append(None)
            e.append(0)

    e[real] = (esum - sum(e)) % (pow(2, PRIME_SIZE))
    z[real] = (r * pow(v, e[real], n * n)) % (n * n)

    return (u, a, e, z, esum)

def check_proof(pk, u, a, e, z, esum):
    n = pk.n
    if (sum(e) % pow(2, PRIME_SIZE)) != esum:
        return False

    for i in range(len(u)):
        if (pow(z[i], n, n * n) != (a[i] * pow(u[i], e[i], n * n)) % (n * n)):
            return False

    return True
