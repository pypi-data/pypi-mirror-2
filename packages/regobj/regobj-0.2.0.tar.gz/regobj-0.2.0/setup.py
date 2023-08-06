#
#  This is the regobj setuptools script.
#  Originally developed by Ryan Kelly, 2009.
#
#  This script is placed in the public domain.
#

from distutils.core import setup

#  If we did a straight `import regobj` here we wouldn't be able
#  to build on non-win32 machines.
regobj = {}
try:
    execfile("regobj.py",regobj)
except ImportError:
    pass
VERSION = regobj["__version__"]

NAME = "regobj"
DESCRIPTION = "Pythonic object-based access to the Windows Registry."
LONG_DESC = regobj["__doc__"]
AUTHOR = "Ryan Kelly"
AUTHOR_EMAIL = "ryan@rfk.id.au"
URL="https://github.com/rfk/regobj"
LICENSE = "MIT"
KEYWORDS = "windows registry"

setup(name=NAME,
      version=VERSION,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      url=URL,
      description=DESCRIPTION,
      long_description=LONG_DESC,
      license=LICENSE,
      keywords=KEYWORDS,
      py_modules=["regobj"],
      classifiers=[c.strip() for c in """
        Intended Audience :: Developers
        License :: OSI Approved :: MIT License
        Programming Language :: Python :: 2
        Programming Language :: Python :: 3
        Topic :: Software Development :: Libraries :: Python Modules
        """.split('\n') if c.strip()],
     )

