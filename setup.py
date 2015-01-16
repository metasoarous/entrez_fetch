from distutils.core import setup

from sekhon import __version__

setup(name='entrez_fetch',
        version=__version__,
        author="Christopher Small",
        scripts=['entrez_fetch.py'],
        py_modules=['entrez_fetch'],
        requires=['biopython'])

