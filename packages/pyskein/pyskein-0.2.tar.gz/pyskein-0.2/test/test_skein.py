import unittest
import re

import skein

KATFILE = "skein_golden_kat.txt"


class TestCipherBase(unittest.TestCase):
    def setUp(self):
        self.hasher = skein.skein512()

    def testMultipleDigests(self):
        self.assertEqual(self.hasher.digest(), self.hasher.digest())
        self.assertEqual(self.hasher.hexdigest(), self.hasher.hexdigest())

    def testHexDigest(self):
        st = "".join(format(b, "02x") for b in self.hasher.digest())
        self.assertEqual(self.hasher.hexdigest(), st)

    def testInit(self):
        self.hasher.update(b"\xff")
        hasher2 = skein.skein512(b"\xff")
        self.assertEqual(hasher2.digest(), self.hasher.digest())

    def testCopy(self):
        self.hasher.update(b"1")
        copy = self.hasher.copy()
        hash1 = self.hasher.digest()
        self.hasher.update(b"2")
        self.assertNotEqual(hash1, self.hasher.digest())
        self.assertEqual(hash1, copy.digest())

    def testDigestSizes(self):
        self.assertRaises(ValueError, skein.skein256, b"", 7)
        self.assertRaises(ValueError, skein.skein512, b"", 0)
        self.assertRaises(ValueError, skein.skein1024, b"", -1)

    def testAttributes(self):
        for state_bits, factory in ((256, skein.skein256),
                                    (512, skein.skein512),
                                    (1024, skein.skein1024)):
            for digest_bits in range(8, 1025, 8):
                hasher = factory(digest_bits=digest_bits)
                self.assertEqual(hasher.block_size*8, state_bits)
                self.assertEqual(hasher.block_bits, state_bits)
                self.assertEqual(hasher.digest_size*8, digest_bits)
                self.assertEqual(hasher.digest_bits, digest_bits)
                self.assertEqual(hasher.name, "Skein-{0}".format(state_bits))


def by(txt):
    if "(none)" in txt:
        return bytes()
    lines = [line for line in txt.split("\n") if line.startswith("   ")]
    txt = "".join(lines)
    return bytes(int(x, 16) for x in txt.split())

class TestKAT(unittest.TestCase):
    RE_HEADER = re.compile(r":Skein-(\d+):\s+(\d+)-bit hash, "+
                           r"msgLen =\s+(\d+) bits, data")

    def runTest(self):
        with open(KATFILE, "r") as f:
            kattxt = f.read()
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


if __name__ == "__main__":
    unittest.main()
