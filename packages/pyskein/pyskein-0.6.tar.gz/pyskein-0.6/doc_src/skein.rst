Computing Skein hashes
======================

A new hash object is created by one of the following three functions:

.. function:: skein.skein256(init=b'', digest_bits=256, mac=b'', pers=b'', nonce=b'', tree=None)
.. function:: skein.skein512(init=b'', digest_bits=512, mac=b'', pers=b'', nonce=b'', tree=None)
.. function:: skein.skein1024(init=b'', digest_bits=1024, mac=b'', pers=b'', nonce=b'', tree=None)

    These constructor functions return a corresponding hash object
    for Skein-256, Skein-512, or Skein-1024 (i.e. 256, 512, or 1024 bits
    internal state).  They optionally take an initial chunk of data to hash
    (`init`) and the desired digest length in bits (`digest_bits`,
    must be a multiple of 8 and < 2**31).

    Further optional parameters are:

        * `mac`: a key for use of Skein as a MAC, arbitrary bytes
        * `pers`: a personalization string, arbitrary bytes
        * `nonce`: a nonce value, arbitrary bytes
        * `tree`: tree hashing parameters, tuple of exponents: (leaf, fan_out, max_height)

    Specifying these four parameters as positional arguments is deprecated -
    please use them as keyword arguments only!
    For details about their meaning please consult the `Skein specification`_.

.. _`Skein specification`: http://www.skein-hash.info/sites/default/files/skein1.2.pdf


Hash objects
------------

Hash objects have the following methods:

.. method:: update(data)

   Hash the given chunk of (bytes) data into the internal state.
   (String data has to be encoded to bytes first.)
   Repeated calls are equivalent to a single call with the concatenation
   of all the arguments.

.. method:: digest

   Return the digest of all data processed so far. This is a bytes object
   of length :attr:`digest_size`.

.. method:: hexdigest

   Like :meth:`digest`, but returning the digest as a string
   of hexadecimal digits.

.. method:: copy

   Return a clone of the hash object, e.g. to efficiently compute hashes of
   data sharing a common prefix.


In addition each hash object has the following attributes:

.. attribute:: name

   Name of the algorithm, i.e. ``'Skein-256'``, ``'Skein-512'``, or
   ``'Skein-1024'``.

.. attribute:: block_bits

   Internal state size in bits, i.e. ``256``, ``512``, or ``1024``.

.. attribute:: block_size

   Internal state size in bytes (conforming to :mod:`hashlib`),
   i.e. ``32``, ``64``, or ``128``.

.. attribute:: digest_bits

   Output digest length in bits, i.e. the value given to the constructor
   function (or default).

.. attribute:: digest_size

   Digest size in bytes.


Simple examples
---------------

Make a Skein-512 hash object with default digest length (512 bits)
and hash some data::

    >>> from skein import skein256, skein512, skein1024
    >>> h = skein512()
    >>> h.update(b'Nobody inspects')
    >>> h.update(b' the spammish repetition')
    >>> h.digest()
    b'\xad\xd2\xc32\x8a \xa6\xfc\xeb\x89i\xcbr\x0e\xa3\x83~>\x9e\x1e%\xfb\x17\x8f\xa8h8\xbb\x8f\xac\x8f\xf6\x84\xbb~\x02\x0cZ\xdbK\x89:b\x84\x9dWq\x0c\x9f\x8c\xc65\xc6k>HZ\x9a\xbd$\x9f39\x1e'
    >>> h.digest_size, h.digest_bits
    (64, 512)
    >>> h.block_size, h.block_bits
    (64, 512)

Similarly for Skein-1024-384::

    >>> h = skein1024(b'Nobody inspects the spammish repetition', digest_bits=384)
    >>> h.hexdigest()
    'ee9c327d52b960fe443885c8000508d3ce5ef0700d3e5d7646b5c99605dbb327c8bcd5a93b3dbe5c439243795c7bf780'
    >>> h.digest_size, h.digest_bits
    (48, 384)
    >>> h.block_size, h.block_bits
    (128, 1024)


Advanced examples
-----------------

Hashing with a MAC key, a personalization string or a nonce value (or all of
them) changes the digest::

    >>> skein256(b'message').hexdigest()
    '23f5b683765f67bd3d8de82938a949f1b5bc83b83ee4d621b5d74fff5c40c8e9'
    >>> skein256(b'message', mac=b'foobar').hexdigest()
    '283299f2ef51392b312193478a520402b53f3ea79605d3daa42251daff8709e8'
    >>> skein256(b'message', pers=b'foobar').hexdigest()
    '4afd97f1f703bc9dff89a2a189171e935c15598ce74df0639d080cbd5e76cdee'
    >>> skein256(b'message', nonce=b'foobar').hexdigest()
    'dd265cda71330e4c5c8efe95763d1fe76cd1603ca80f8da5819ac6de664772f1'
    >>> skein256(b'message', mac=b'foo', pers=b'bar', nonce=b'baz').hexdigest()
    '58da697148a1b26332197015ba618a61beab1452dc0ddefbe227bf5ccd684451'

Tree hashing uses the same incremental interface as sequential hashing. To hash
with a leaf size of 2**L blocks, a fan-out of 2**F children per node and a
maximum tree height of M, simply specify a `tree` parameter of (L, F, M)::

    >>> h = skein256(tree=(5, 2, 255))
    >>> for _ in range(1000):
    ...     h.update(b'\0' * 10**6)
    ...
    >>> h.update(b'foobar')
    >>> h.hexdigest()
    '2c1531d8e1b7d28de7c3e47085d94738270f0d05bfb40e87b8613b05792828cf'

A future version of PySkein will parallelize tree hashing for higher
performance on multi-core systems.
