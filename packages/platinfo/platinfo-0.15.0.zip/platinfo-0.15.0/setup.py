#!/usr/bin/env python

import os
import sys
import distutils
from distutils.core import setup

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))
try:
    import platinfo
finally:
    del sys.path[0]

classifiers = """\
Development Status :: 5 - Production/Stable
Intended Audience :: Developers
License :: OSI Approved :: MIT License
Programming Language :: Python
Programming Language :: Python :: 2.4
Programming Language :: Python :: 2.5
Programming Language :: Python :: 2.6
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3
Operating System :: OS Independent
Topic :: Software Development :: Libraries :: Python Modules
"""

doclines = open(os.path.join(os.path.dirname(__file__), "README.txt")).read().split("\n")
script = (sys.platform == "win32" and "lib\\platinfo.py" or "bin/platinfo")

setup(
    name="platinfo",
    version=platinfo.__version__,
    maintainer="Trent Mick",
    maintainer_email="trentm@gmail.com",
    url="http://code.google.com/p/platinfo/",
    license="http://www.opensource.org/licenses/mit-license.php",
    platforms=["any"],
    py_modules=["platinfo"],
    package_dir={"": "lib"},
    scripts=[script],
    description=doclines[0],
    classifiers=filter(None, classifiers.split("\n")),
    long_description="\n".join(doclines[2:]),
)

