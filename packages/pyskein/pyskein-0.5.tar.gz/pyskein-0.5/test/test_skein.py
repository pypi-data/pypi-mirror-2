import sys
import re
import random
import unittest
from itertools import combinations

import skein

KATFILE = "skein_golden_kat.txt"


class TestSkeinModule(unittest.TestCase):
    def test(self):
        self.assertEqual(type(skein.__version__), str)


class TestSkeinBase:
    def setUp(self):
        self.hasher = self.HASHER()

    def testMultipleDigests(self):
        self.assertEqual(self.hasher.digest(), self.hasher.digest())
        self.assertEqual(self.hasher.hexdigest(), self.hasher.hexdigest())

    def testHexDigest(self):
        st = "".join(format(b, "02x") for b in self.hasher.digest())
        self.assertEqual(self.hasher.hexdigest(), st)

    def testInit(self):
        self.hasher.update(b"\xff")
        hasher2 = self.HASHER(b"\xff")
        self.assertEqual(hasher2.digest(), self.hasher.digest())

    def testCopy(self):
        self.hasher.update(b"1")
        copy = self.hasher.copy()
        hash1 = self.hasher.digest()
        self.hasher.update(b"2")
        self.assertNotEqual(hash1, self.hasher.digest())
        self.assertEqual(hash1, copy.digest())

    def testDigestSizes(self):
        self.assertRaises(ValueError, self.HASHER, b"", 7)
        self.assertRaises(ValueError, self.HASHER, b"", 0)
        self.assertRaises(ValueError, self.HASHER, b"", -1)

    def testAttributes(self):
        for digest_bits in range(8, 2049, 8):
            hasher = self.HASHER(digest_bits=digest_bits)
            self.assertEqual(hasher.block_size*8, self.STATE_BITS)
            self.assertEqual(hasher.block_bits, self.STATE_BITS)
            self.assertEqual(hasher.digest_size*8, digest_bits)
            self.assertEqual(hasher.digest_bits, digest_bits)
            self.assertEqual(hasher.name, "Skein-{0}".format(self.STATE_BITS))

    def testInitArgCombinations(self):
        for n in range(6):
            for kws in combinations(["init", "digest_bits",
                                     "mac", "pers", "nonce"], n):
                kwdict = {kw:b"bar"+bytes([i]) if kw != "digest_bits" else 256
                          for i, kw in enumerate(kws)}
                self.HASHER(**kwdict)

    def testEmptyInitArgs(self):
        hash = self.HASHER(b"foo").digest()
        self.assertEqual(self.HASHER(b"foo", mac=b"").digest(), hash)
        self.assertEqual(self.HASHER(b"foo", pers=b"").digest(), hash)
        self.assertEqual(self.HASHER(b"foo", nonce=b"").digest(), hash)
        self.assertEqual(self.HASHER(b"foo", pers=b"", nonce=b"").digest(),
                         hash)

class TestSkein256(TestSkeinBase, unittest.TestCase):
    HASHER = skein.skein256
    STATE_BITS = 256

class TestSkein512(TestSkeinBase, unittest.TestCase):
    HASHER = skein.skein512
    STATE_BITS = 512

class TestSkein1024(TestSkeinBase, unittest.TestCase):
    HASHER = skein.skein1024
    STATE_BITS = 1024


class TestSkeinKAT(unittest.TestCase):
    RE_HEADER = re.compile(r":Skein-(\d+):\s+(\d+)-bit hash, "+
                           r"msgLen =\s+(\d+) bits, data")

    def runTest(self):
        with open(KATFILE, "r") as f:
            kattxt = f.read()
        n = 0
        for block in kattxt.split("---------\n"):
            m = self.RE_HEADER.search(block)
            if m is None:
                continue
            state_bits, digest_bits, msg_bits = map(int, m.groups())
            if msg_bits%8 != 0:
                continue
            block = block.split("Message data:\n", 1)[1]
            if "MAC key =" in block:
                msgtxt, block = block.split("MAC key =", 1)
                check, block = block.split("\n", 1)
                check = int(check.split()[0])
                mactxt, hashtxt = block.split("Result:\n")
            else:
                msgtxt, hashtxt = block.split("Result:\n")
                mactxt = ""
            if state_bits == 256:
                hasher = skein.skein256
            elif state_bits == 512:
                hasher = skein.skein512
            elif state_bits == 1024:
                hasher = skein.skein1024
            digest = hasher(by(msgtxt), digest_bits=digest_bits,
                            mac=by(mactxt)).digest()
            self.assertEqual(digest, by(hashtxt))
            n += 1
        print("\nAll {0} applicable known answer tests succeeded.".format(n))

def by(txt):
    if "(none)" in txt:
        return bytes()
    lines = [line for line in txt.split("\n") if line.startswith("   ")]
    txt = "".join(lines)
    return bytes(int(x, 16) for x in txt.split())


class TestThreefishBase:
    def setUp(self):
        self.t = skein.threefish(bytes(range(self.KEYLEN)),
                                 bytes(range(16)))
        # create a distractor object for strange string buffer false positives:
        skein.threefish(bytes(range(self.KEYLEN)), bytes(range(11, 27)))

    def test_attributes(self):
        self.assertEqual(self.t.block_size, self.KEYLEN)
        self.assertEqual(self.t.block_bits, self.KEYLEN*8)
        self.assertEqual(self.t.tweak, bytes(range(16)))

    def test_tweak(self):
        def set(v):
            self.t.tweak = v
        self.assertRaises(TypeError, set, 0)
        self.assertRaises(ValueError, set, bytes(17))
        set(bytes(range(1, 17)))
        self.assertEqual(self.t.tweak, bytes(range(1, 17)))

    def test_encrypt_block(self):
        self.assertRaises(ValueError,
                          self.t.encrypt_block, bytes(1))
        self.assertRaises(ValueError,
                          self.t.encrypt_block, bytes(self.KEYLEN+1))
        self.assertRaises(ValueError,
                          self.t.encrypt_block, bytes(self.KEYLEN-1))

    def test_decrypt_block(self):
        self.assertRaises(ValueError,
                          self.t.decrypt_block, bytes(1))
        self.assertRaises(ValueError,
                          self.t.decrypt_block, bytes(self.KEYLEN+1))
        self.assertRaises(ValueError,
                          self.t.decrypt_block, bytes(self.KEYLEN-1))

    def test_roundtrip(self):
        for n in range(1, 101):
            key = bytes(random.randint(0, 255) for _ in range(self.KEYLEN))
            tweak = bytes(random.randint(0, 255) for _ in range(16))
            plain = bytes(random.randint(0, 255) for _ in range(self.KEYLEN))
            t = skein.threefish(key, tweak)
            self.assertEqual(t.decrypt_block(t.encrypt_block(plain)), plain)
        print("\n{0} random Threefish{1} roundtrip tests succeeded.".format(
              n, self.KEYLEN))

class TestThreefish32(TestThreefishBase, unittest.TestCase):
    KEYLEN = 32

class TestThreefish64(TestThreefishBase, unittest.TestCase):
    KEYLEN = 64

class TestThreefish128(TestThreefishBase, unittest.TestCase):
    KEYLEN = 128


class TestPRNG(unittest.TestCase):
    def test_init(self):
        skein.Random()
        skein.Random(42)
        skein.Random(frozenset({1,2,3}))
        skein.Random("str")

    def setUp(self):
        self.r = skein.Random(b"x")

    def testStateInspection(self):
        # check initial state
        state = self.r._state
        d = skein.skein512(bytes(64)+b"x", digest_bits=512).digest()
        self.assertEqual(state, d)

        # check state after random() call
        self.r.random()
        d = skein.skein512(state, digest_bits=512+80*53).digest()
        self.assertEqual(self.r._state, d[:64])

    def testNumbers(self):
        lst = [self.r.randrange(10) for _ in range(10)]
        self.assertEqual(lst, [8, 7, 0, 8, 9, 0, 1, 1, 3, 4])

    def testGetSetState(self):
        self.r.random()
        self.r.gauss(0, 1)
        state = self.r.getstate()
        a = self.r.random()
        b = self.r.gauss(0, 1)
        self.r.setstate(state)
        self.assertEqual(self.r.random(), a)
        self.assertEqual(self.r.gauss(0, 1), b)


if __name__ == "__main__":
    t = unittest.defaultTestLoader.loadTestsFromModule(sys.modules["__main__"])
    r = unittest.TextTestRunner()
    r.run(t)
    if hasattr(sys, "gettotalrefcount"):
        refc = sys.gettotalrefcount()
        for i in range(10):
            r.run(t)
            print("additional references:", sys.gettotalrefcount()-refc)

