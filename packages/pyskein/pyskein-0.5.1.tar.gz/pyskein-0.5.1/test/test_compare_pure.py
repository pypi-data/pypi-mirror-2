import skein512
import skein
import random
import unittest


class TestThreefish(unittest.TestCase):
    def runTest(self):
        for i in range(100):
            key = randombytes(64)
            tweak = randombytes(16)
            plain = randombytes(64)
            gold = skein512.threefish(key, tweak, plain)
            c = skein.threefish(key, tweak)
            self.assertEqual(c.encrypt_block(plain), gold)


class TestSkein(unittest.TestCase):
    def runTest(self):
        for msg in randomlist():
            for mac in randomlist():
                for pers in randomlist():
                    for nonce in randomlist():
                        gold = skein512.skein512(msg, mac, pers, nonce)
                        c = skein.skein512(msg, mac=mac,
                                           pers=pers, nonce=nonce)
                        self.assertEqual(c.digest(), gold)


def randombytes(n):
    return bytes(random.randint(0, 255) for _ in range(n))


def randomlist():
    return [b"", randombytes(random.randint(1, 10)),
            randombytes(random.randint(100, 1000))]


if __name__ == "__main__":
    unittest.main()
