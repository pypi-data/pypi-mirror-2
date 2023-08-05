# -*- encoding: utf-8
import sys
if sys.version_info[0] < 3:
    print("Python version >= 3.0 required!\n")
    sys.exit(1)


from distutils.core import setup, Extension

ext = Extension("skein",
                sources=["src/skein_block.c", "src/skein.c", "src/threefish.c",
                         "src/skeinmodule.c"],
                include_dirs=["src"])
pyskein_url = "http://www.coli.uni-saarland.de/~hagenf/personal/pyskein"
setup(name="pyskein",
      version="0.3",
      description="Efficiently compute Skein hashes",
      author="Hagen Fürstenau",
      author_email="hfuerstenau@gmx.net",
      license="GPL",
      platforms=["Linux", "Windows"],
      url=pyskein_url,
      classifiers=[
          "Development Status :: 4 - Beta",
          "Intended Audience :: Developers",
          "Intended Audience :: Science/Research",
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "Operating System :: Microsoft :: Windows",
          "Operating System :: Unix",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.0",
          "Topic :: Security :: Cryptography"],
      ext_modules=[ext])
