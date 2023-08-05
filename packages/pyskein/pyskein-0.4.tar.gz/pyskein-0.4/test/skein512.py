# Pure Python implementation of Skein-512.  Requires Python >=3.0.
# Written by Hagen Fürstenau, released to the public domain.

### bytes <--> words conversions ###

def BytesToWords(b, n):
    """Return n words for 8*n bytes."""
    return [sum(b[8*i+j]<<(8*j) for j in range(8)) for i in range(n)]

def WordsToBytes(w):
    """Return 8*n bytes for n words."""
    return bytearray((v>>(8*j))&255 for v in w for j in range(8))


### MIX function and inverse ###

R = [[38, 30, 50, 53],
     [48, 20, 43, 31],
     [34, 14, 15, 27],
     [26, 12, 58, 7],
     [33, 49, 8, 42],
     [39, 27, 41, 14],
     [29, 26, 11, 9],
     [33, 51, 39, 35]]

def mix(d, j, x0, x1):
    r = R[d%8][j]
    y0 = (x0+x1) & (2**64-1)
    y1 = ((x1<<r) | (x1>>(64-r))) & (2**64-1)
    y1 ^= y0
    return y0, y1

def mix_inv(d, j, y0, y1):
    r = R[d%8][j]
    y1 ^= y0
    x1 = (y1>>r) | (y1<<(64-r)) & (2**64-1)
    x0 = (y0-x1) & (2**64-1)
    return x0, x1


### Threefish ###

def subkeys(k, t):
    ek = 2**64//3
    for kw in k:
        ek ^= kw
    k.append(ek)
    t.append(t[0]^t[1])
    for s in range(19):
        sk = [k[(s+i)%9] for i in range(5)]
        sk.append((k[(s+5)%9]+t[s%3]) & (2**64-1))
        sk.append((k[(s+6)%9]+t[(s+1)%3]) & (2**64-1))
        sk.append((k[(s+7)%9]+s) & (2**64-1))
        yield sk

PI = [2, 1, 4, 7, 6, 5, 0, 3]
def threefish(key, tweak, plain):
    """'key' and 'plain' contain 64 bytes, 'tweak' contains 16 bytes."""
    k = BytesToWords(key, 8)
    t = BytesToWords(tweak, 2)
    v = BytesToWords(plain, 8)
    f = [0]*8
    d = 0
    for sk in subkeys(k, t):
        for i in range(8):
            v[i] = (v[i]+sk[i]) & (2**64-1)
        if d == 72:
            break
        for _ in range(4):
            for j in range(4):
                f[2*j], f[2*j+1] = mix(d, j, v[2*j], v[2*j+1])
            for i in range(8):
                v[i] = f[PI[i]]
            d += 1
    return WordsToBytes(v)

def threefish_decrypt(key, tweak, encrypted):
    """'key' and 'plain' contain 64 bytes, 'tweak' contains 16 bytes."""
    k = BytesToWords(key, 8)
    t = BytesToWords(tweak, 2)
    v = BytesToWords(encrypted, 8)
    f = [0]*8
    d = 72
    for sk in reversed(list(subkeys(k, t))):
        for i in range(8):
            v[i] = (v[i]-sk[i]) & (2**64-1)
        if d == 0:
            break
        for _ in range(4):
            d -= 1
            for i in range(8):
                f[PI[i]] = v[i]
            for j in range(4):
                v[2*j], v[2*j+1] = mix_inv(d, j, f[2*j], f[2*j+1])
    return WordsToBytes(v)


### Skein ###

def ubi(g, m, ts):
    m = bytearray(m)
    l = len(m)
    if (l == 0) or (l%64 != 0):
        m.extend([0]*(64-l%64))
    h = bytearray(g)
    ts_pos = ts
    for i in range(0, len(m), 64):
        block = m[i:i+64]
        ts_pos += 64
        tweak = ts_pos
        if i == 0:
            tweak |= 1<<126
        if i == len(m)-64:
            tweak |= 1<<127
            tweak -= len(m)-l
        tweak_bytes = WordsToBytes([tweak&(2**64-1), tweak>>64])
        cipher = threefish(h, tweak_bytes, block)
        h = bytearray(x^y for x, y in zip(cipher, block))
    return h

# With the '+ 32*b"\0"' part the CONFIG string reproduces
# the bug in version 1.0 of the reference implementation.
CONFIG = b"SHA3\1\0\0\0\0\2\0\0\0\0\0\0\0\0\0" + 13*b"\0" #+ 32*b"\0"
def skein512(msg, mac=b"", pers=b"", nonce=b""):
    g = b"\0"*64
    if mac:
        g = ubi(g, mac, 0)
    g = ubi(g, CONFIG, 4<<120)
    if pers:
        g = ubi(g, pers, 8<<120)
    if nonce:
        g = ubi(g, nonce, 20<<120)
    g = ubi(g, msg, 48<<120)
    return ubi(g, b"\0"*8, 63<<120)


### Print hash of MSG if called directly ###
if __name__ == "__main__":
    MSG = b"Nobody inspects the spammish repetition"
    hash = skein512(MSG)
    print(":Skein-512:   512-bit hash, msgLen = {0:5} bits".format(len(MSG)*8))
    print("\nMessage:", MSG)
    print("Result:")
    for i in range(0, len(hash), 16):
        print("     ", end="")
        for j in range(i, i+16, 4):
            print(" ".join(format(b, "02X") for b in hash[j:j+4]), end="  ")
        print()
