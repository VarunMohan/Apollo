import Crypto.Util.number as pycrypto
from crypto import constants
from crypto import paillier

PRIME_SIZE = constants.PRIME_SIZE


# takes in a public key pk, sequence of cipher texts u, sum of e's (random number),
# index of the real cipher text and the random number used for the vote v
# generates a proof that at least one ciphertext is real
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

# checks the validity of a proof that at least one cipher text is real by verifying that
# sum e = esum
# z_i^n = a_i * u_i^e_i
def check_proof(pk, u, a, e, z, esum):
    n = pk.n
    if (sum(e) % pow(2, PRIME_SIZE)) != esum:
        return False

    for i in range(len(u)):
        if (pow(z[i], n, n * n) != (a[i] * pow(u[i], e[i], n * n)) % (n * n)):
            return False

    return True

# generates a ZNP that decryption was done properly, given a random number chal by voter
def decrypt_proof(pk, sk, cipher, chal):
    n = pk.n
    msg = paillier.decrypt(pk, sk, cipher)
    rn = (cipher * pycrypto.inverse(pow(pk.g, msg, n * n), n * n)) % (n * n)
    r = pow(rn, pycrypto.inverse(n, sk.l), n * n) # generates bogus if r^n not nth power
    
    rand = pycrypto.getRandomInteger(PRIME_SIZE * 2)
    randn = pow(rand, n, n * n)
    
    z = rand * pow(r, chal, n * n)
    
    return (msg, cipher, randn, chall, z)

# given a proof, checks decryption was done properly
def check_decrypt(pk, msg, cipher, rand, chall, z):
    n = pk.n
    if pow(z, n, n * n) == ((rand * pow((cipher * pycrypto.inverse(pow(pk.g, msg, n * n), n * n)), chall, n * n))) % (n * n)):
        return True

    return False
    
