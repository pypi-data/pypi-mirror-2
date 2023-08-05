Download PySkein
================

PySkein was mainly tested on 64-bit Linux, but should run on various platforms
supported by Python. Due to the design of the Skein algorithm, performance is
significantly reduced on 32-bit systems.

Download the most recent version 0.6.1:

    * **Source code:** `pyskein-0.6.1.tar.gz <http://pypi.python.org/packages/source/p/pyskein/pyskein-0.6.1.tar.gz>`_ (`sig <http://pypi.python.org/packages/source/p/pyskein/pyskein-0.6.1.tar.gz.asc>`_)

Note: If you have a version of PySkein <0.5 installed, please make sure to
manually delete "skein.*" from your Python `site-packages` directory before
installing a more recent version!


Changes between version
-----------------------

0.6.1
    - Fixed a bug in copy()ing tree hash objects

    - Made hash objects picklable

    - Improved repr() of hash objects

    - Fixed several issues with Python 3.0

0.6
    - Incremental tree hashing with arbitrary tree parameters

    - Restricted digest_bits to < 2^31 bits (256 MB!)

    - Disabled precomputed IVs (their performance benefit is negligible)

    - Deprecated all non-keyword arguments of skein*() functions
      except 'init' and 'digest_bits'

0.5.2
    - Release the GIL to allow multiple threads to hash in parallel
      on multi-core systems

0.5.1
    - Fixed reference leak when changing tweak value on threefish object

0.5
    - Updated rotation constants to new Skein specification (version 1.2)

    - Added implementation of Skein PRNG

0.4
    - Hashing with personalization string

    - Hashing with nonce value

0.3.1
    - Improved demo script "threefish"

    - Better compatibility with Python 3.1

0.3
    - Threefish block decryption

    - Demo scripts "skeinsum" and "threefish"

0.2
    - Support for message authentication codes

    - Threefish block encryption (but no decryption)

    - Fixed one or two reference leaks

0.1
    - Skein-256, Skein-512, and Skein-1024 hashing


Previous versions
-----------------

* `pyskein-0.6.tar.gz <http://pypi.python.org/packages/source/p/pyskein/pyskein-0.6.tar.gz>`_ (`sig <http://pypi.python.org/packages/source/p/pyskein/pyskein-0.6.tar.gz.asc>`_)

* `pyskein-0.5.2.tar.gz <http://pypi.python.org/packages/source/p/pyskein/pyskein-0.5.2.tar.gz>`_ (`sig <http://pypi.python.org/packages/source/p/pyskein/pyskein-0.5.2.tar.gz.asc>`_)

* `pyskein-0.5.2.win32-py3.1.msi <http://pypi.python.org/packages/3.1/p/pyskein/pyskein-0.5.2.win32-py3.1.msi>`_ (`sig <http://pypi.python.org/packages/3.1/p/pyskein/pyskein-0.5.2.win32-py3.1.msi.asc>`_)

* `pyskein-0.5.1.tar.gz <http://pypi.python.org/packages/source/p/pyskein/pyskein-0.5.1.tar.gz>`_ (`sig <http://pypi.python.org/packages/source/p/pyskein/pyskein-0.5.1.tar.gz.asc>`_)

* `pyskein-0.5.tar.gz <http://pypi.python.org/packages/source/p/pyskein/pyskein-0.5.tar.gz>`_ (`sig <http://pypi.python.org/packages/source/p/pyskein/pyskein-0.5.tar.gz.asc>`_)

* `pyskein-0.4.tar.gz <http://pypi.python.org/packages/source/p/pyskein/pyskein-0.4.tar.gz>`_ (`sig <http://pypi.python.org/packages/source/p/pyskein/pyskein-0.4.tar.gz.asc>`_)

* `pyskein-0.3.1.tar.gz <http://pypi.python.org/packages/source/p/pyskein/pyskein-0.3.1.tar.gz>`_ (`sig <http://pypi.python.org/packages/source/p/pyskein/pyskein-0.3.1.tar.gz.asc>`_)

* `pyskein-0.3.tar.gz <http://pypi.python.org/packages/source/p/pyskein/pyskein-0.3.tar.gz>`_ (`sig <http://pypi.python.org/packages/source/p/pyskein/pyskein-0.3.tar.gz.asc>`_)

* `pyskein-0.2.tar.gz <http://pypi.python.org/packages/source/p/pyskein/pyskein-0.2.tar.gz>`_ (`sig <http://pypi.python.org/packages/source/p/pyskein/pyskein-0.2.tar.gz.asc>`_)

* `pyskein-0.1.tar.gz <http://pypi.python.org/packages/source/p/pyskein/pyskein-0.1.tar.gz>`_ (`sig <http://pypi.python.org/packages/source/p/pyskein/pyskein-0.1.tar.gz.asc>`_)

All versions of PySkein <0.5 compute Skein hashes according to an older
specification of Skein (version 1.1). Starting with PySkein 0.5, hashes are
computed according to the current specification with updated rotation constants
(version 1.2). This leads to different hash outputs.
