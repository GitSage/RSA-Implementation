# @author Benjamin Yocum

# generates safe arbitrary length primes using openssl.
# install with pip install https://pypi.python.org/packages/source/g/gensafeprime/gensafeprime-1.5.tar.gz
import gensafeprime
from itertools import combinations


def mod_exp(val, exp, mod_val):
    g_tmp = val
    val_tmp = exp
    x = 1
    while val_tmp > 0:
        if val_tmp % 2 == 0:
            g_tmp = (g_tmp * g_tmp) % mod_val
            val_tmp /= 2
        else:
            x = (g_tmp * x) % mod_val
            val_tmp -= 1
    return x


def coprime(l):
    for i, j in combinations(l, 2):
        if euclid(i, j) != 1:
            return False
    return True


def mod_inv(x, y):
    if coprime([x, y]):
        lin_com = extended_euclid(x, y)
        return lin_com[1] % y
    else:
        return 0


def euclid(x, y):
    x = abs(x)
    y = abs(y)
    if x < y:
        x, y = y, x
    while y != 0:
        x, y = y, x % y
    return x


def extended_euclid(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = extended_euclid(b % a, a)
        return g, x - (b // a) * y, y


if __name__ == '__main__':

    # generate key params
    bitlen = 512
    e = 65537
    p = gensafeprime.generate(bitlen)
    q = gensafeprime.generate(bitlen)
    n = p * q
    m = (p - 1) * (q - 1)
    while not coprime([e, m]):
        p = gensafeprime.generate(bitlen)
        q = gensafeprime.generate(bitlen)
        n = p * q
        m = (p - 1) * (q - 1)
    d = mod_inv(e, m)

    print("p: " + str(p))
    print("q: " + str(q))
    print("n: " + str(n))
    print("e: " + str(e))
    print("d: " + str(d))

    message = int(input("Enter message to encrypt: "))
    cipher = mod_exp(message, e, n)
    print("Encrypted message " + str(cipher))

    cipher = int(input("Enter cipher to decrypt: "))
    deciphered = mod_exp(cipher, d, n)
    print("decrypted message " + str(deciphered))