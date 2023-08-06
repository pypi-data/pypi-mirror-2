# -*- coding: utf-8 -*-
from distutils.core import setup, Extension

LONG_DESCRIPTION = '\
This is an interface to open(), read(), write() and close() on a direct I/O \
context (O_DIRECT flag) from the Python programming language.\n\
\n\
These system calls are Linux system calls to\n\
* open a file with the O_DIRECT flag, and close it.\n\
* read or write from the file ignores the buffer cache.\n\
\n\
The O_DIRECT flag introduced in SGI IRIX, where it has alignment \
restrictions similar to those of Linux 2.4. FreeBSD 4.x introduced a \
flag of the same name, but without alignment restrictions. Support was \
added under Linux in kernel version 2.4.10. Older Linux kernels simply \
ignore this flag.\n\
'

classifiers = """\
Development Status :: 3 - Alpha
Intended Audience :: Developers
License :: OSI Approved :: GNU General Public License (GPL)
Programming Language :: Python
Topic :: Software Development :: Libraries :: Python Modules
Operating System :: POSIX :: Linux
"""

module1 = Extension('directio',
                    sources = ['directiomodule.c'])

setup (name = 'directio',
       version = '1.1',
       author = u'Omar Ait Mous, Jérôme Petazzoni',
       author_email = 'dev.python.directio@enix.fr',
       maintainer = u'Jérôme Petazzoni',
       maintainer_email = 'dev.python.directio@enix.fr',
       url = 'www.enix.org',
       license = 'http://www.gnu.org/licenses/gpl.txt',
       platforms = ['Linux'],
       description = 'A Python interface to open/read/write on a direct I/O \
context.',
       long_description = LONG_DESCRIPTION,
       classifiers = filter(None, classifiers.split("\n")),
       ext_modules = [module1])
