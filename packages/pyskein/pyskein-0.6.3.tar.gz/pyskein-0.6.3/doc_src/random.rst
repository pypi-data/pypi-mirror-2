Pseudorandom Number Generator
=============================

PySkein contains a PRNG designed according to the Skein specification and based
on Skein-512. It is implemented in Python as a subclass of the standard
library's :class:`random.Random` class and can therefore be used in the same
way. The seed may be given as a :class:`bytes` object::

    >>> import skein
    >>> r = skein.Random(b'my seed')
    >>> r.random()
    0.5120516960943258

or any other hashable object - in which case :class:`random.Random` is used
internally to derive a :class:`bytes` seed::

    >>> skein.Random(12345).random()
    0.4814263222592855

The same happens when no seed is given, so that the initial state is then
derived from a suitable system source of randomness (like /dev/urandom or the
time)::

    >>> r = skein.Random()
    >>> r.random()
    0.9696830103216001

All other methods of :class:`skein.Random` are based on :meth:`random()`.
For their documentation please refer to the `Python documentation`_.

.. _`Python documentation`: http://docs.python.org/py3k/
