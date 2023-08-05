# -*- encoding: utf-8
import sys
if sys.version_info[0] < 3:
    print("PySkein requires Python 3.0 or later!\n")
    sys.exit(1)


from distutils.core import setup, Extension

HOMEPAGE = "http://www.coli.uni-saarland.de/~hagenf/personal/pyskein/"


ext = Extension("skein",
                sources=["src/skein_block.c", "src/skein.c", "src/threefish.c",
                         "src/skeinmodule.c"],
                include_dirs=["src"])
setup(name="pyskein",
      version="0.3.1",
      description="Efficiently compute Skein hashes",
      author="Hagen Fürstenau",
      author_email="hfuerstenau@gmx.net",
      license="GPL",
      url=HOMEPAGE,
      classifiers=[
          "Development Status :: 4 - Beta",
          "Intended Audience :: Developers",
          "Intended Audience :: Science/Research",
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "Operating System :: OS Independent",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.0",
          "Programming Language :: Python :: 3.1",
          "Topic :: Security :: Cryptography"],
      ext_modules=[ext],
      scripts=["scripts/skeinsum", "scripts/threefish"])
