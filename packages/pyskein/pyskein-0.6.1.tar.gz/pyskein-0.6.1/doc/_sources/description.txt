PySkein is an extension module for Python 3.0 or later,
implementing the `Skein hash algorithm`_, one of the Second
Round Candidates in the `NIST SHA-3 Competition`_. While
originally based on the optimized version of the reference
implementation by Doug Whiting, PySkein has since evolved into a
feature-rich and pythonic module. It is released as free
software under the `GNU General Public License`_. Its highlights
are:

* A simple **interface** following the hash algorithms in the
  Python standard library (like `hashlib.sha1` or
  `hashlib.sha256`)

* High hashing **performance** through efficient implementation
  in C (368 MB/s on a 2.8 GHz Opteron)

* Many **features** of the Skein specification (such as tree
  hashing, various parameters and output sizes etc.)

* **Threefish**, the tweakable block cipher used in Skein,
  available for encrytion and decryption on its own

.. _`GNU General Public License`: http://www.gnu.org/licenses/gpl-3.0.html
.. _`Skein hash algorithm`: http://www.skein-hash.info
.. _`NIST SHA-3 Competition`: http://csrc.nist.gov/groups/ST/hash/sha-3/index.html
