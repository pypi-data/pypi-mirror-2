Threefish block cipher
======================

.. function:: skein.threefish(key, tweak)

    This constructor function returns a cipher object for encryption and
    decryption with the given key and tweak values.
    The key must be a bytes object of length 32, 64, or 128,
    while the tweak must always consist of 16 bytes.


Threefish objects
-----------------

Threefish cipher objects have two methods:

.. method:: encrypt_block(data)

    Encrypt the given block of (bytes) data.
    (String data has to be encoded to bytes first.)
    The block has to have the same length as the key,
    i.e. 32, 64, or 128 bytes.

.. method:: decrypt_block(data)

    Decrypt the given block of (bytes) data.
    The block has to have the same length as the key,
    i.e. 32, 64, or 128 bytes.


In addition they have the following attributes:

.. attribute:: tweak

    The tweak value given to the constructor function.
    This attribute is writable, allowing the tweak to be changed without
    creation of a new cipher object.

.. attribute:: block_bits

    Threefish block size (as determined by the key length) in bits, i.e.
    ``256``, ``512``, or ``1024``

.. attribute:: block_size

    Threefish block size in bytes (same as the key length), i.e.
    ``32``, ``64``, or ``128``


Examples
--------

Encryption and decryption of a block of 32 bytes::

    >>> from skein import threefish
    >>> t = threefish(b'key of 32,64 or 128 bytes length', b'tweak: 16 bytes ')
    >>> t.block_size, t.block_bits
    (32, 256)
    >>> c = t.encrypt_block(b'block of data,same length as key')
    >>> c
    b"\x166C@\x9b6\xacx\xd3l\xb0\xb3t~\x11\xaa\xbe\x86h'\x95\xd3~W\xd0(\xdd2\xd7\x82k\xd3"
    >>> t.decrypt_block(c)
    b'block of data,same length as key'


Changing the tweak leads to a different cipher text::

    >>> t.tweak = b'some other tweak'
    >>> c = t.encrypt_block(b'block of data,same length as key')
    >>> c
    b"\xd9\xba\xdaq1\xe2's\x02\xfd_\xae\x9f\x84\x03\x7f\xd9\x7f\xf5e\x80\xf4\x1a\xcd\x83\x10\x06P\x13\xee\xdee"
    >>> t.decrypt_block(c)
    b'block of data,same length as key'

