from distutils.core import setup, Extension

ext = Extension("skein",
                sources=["src/skein_block.c", "src/skein.c",
                         "src/skeinmodule.c"],
                include_dirs=["src"])
pyskein_url = "http://www.coli.uni-saarland.de/~hagenf/personal/pyskein"
setup(name="pyskein",
      version="0.2",
      description="Efficiently compute Skein hashes",
      author="Hagen Fürstenau",
      author_email="hfuerstenau@gmx.net",
      license="GPL",
      platforms=["Linux", "Windows"],
      url=pyskein_url,
      classifiers=["Development Status :: 3 - Alpha",
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "Intended Audience :: Developers",
          "Intended Audience :: Science/Research",
          "Operating System :: Unix",
          "Programming Language :: Python :: 3",
          "Topic :: Security :: Cryptography"],
      ext_modules=[ext])
