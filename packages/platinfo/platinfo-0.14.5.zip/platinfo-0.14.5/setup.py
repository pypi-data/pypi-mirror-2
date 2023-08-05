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
Operating System :: OS Independent
Topic :: Software Development :: Libraries :: Python Modules
"""

if sys.version_info < (2, 3):
    # Distutils before Python 2.3 doesn't accept classifiers.
    _setup = setup
    def setup(**kwargs):
        if kwargs.has_key("classifiers"):
            del kwargs["classifiers"]
        _setup(**kwargs)

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

