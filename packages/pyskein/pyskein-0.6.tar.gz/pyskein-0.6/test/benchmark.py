import timeit

COUNT = 10
BLOCK_SIZE = 10 # MB


def hashing_throughput(module, func):
    """Return performance in MB/s"""

    setup = "from {0} import {1} as hasher; update = hasher().update; "\
            "txt = bytes({2})".format(module, func, BLOCK_SIZE*2**20)
    best = min(timeit.repeat("update(txt)", setup, number=COUNT, repeat=5))
    return COUNT*BLOCK_SIZE/best


if __name__ == "__main__":
    hashers = [("hashlib", f) for f in ("md5", "sha1", "sha256", "sha512")]
    hashers += [("skein", f) for f in ("skein256", "skein512", "skein1024")]
    for module, func in hashers:
        x = hashing_throughput(module, func)
        print("{0}.{1}: {2:.3f} MB/s".format(module, func, x))
