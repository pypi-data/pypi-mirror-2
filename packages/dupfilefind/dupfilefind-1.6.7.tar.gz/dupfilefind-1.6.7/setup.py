#!/usr/bin/env python

# dupfilefind -- find files with identical contents
#
# Copyright (C) 2007-2010 Zooko Wilcox-O'Hearn
# Author: Zooko Wilcox-O'Hearn
#
# Permission is hereby granted to any person obtaining a copy of this work to
# deal in this work without restriction (including the rights to use, modify,
# distribute, sublicense, and/or sell copies).

try:
    from ez_setup import use_setuptools
except ImportError:
    pass
else:
    use_setuptools(download_delay=0)

from setuptools import Extension, find_packages, setup

import re, sys

trove_classifiers=[
    "Development Status :: 4 - Beta",
    "Environment :: Console",
    "License :: OSI Approved :: GNU General Public License (GPL)",
    "License :: DFSG approved",
    "Intended Audience :: Developers",
    "Intended Audience :: End Users/Desktop",
    "Intended Audience :: System Administrators",
    "Operating System :: Microsoft",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: Unix",
    "Operating System :: POSIX :: Linux",
    "Operating System :: POSIX",
    "Operating System :: MacOS :: MacOS X",
    "Operating System :: Microsoft :: Windows :: Windows NT/2000",
    "Operating System :: OS Independent",
    "Natural Language :: English",
    "Programming Language :: Python",
    "Topic :: Utilities",
    "Topic :: System :: Systems Administration",
    "Topic :: System :: Filesystems",
    "Topic :: System :: Archiving :: Backup",
    "Topic :: System :: Archiving :: Mirroring",
    "Topic :: System :: Archiving",
    ]

VERSIONFILE = "dupfilefind/_version.py"
verstr = "unknown"
VSRE = re.compile("^verstr = ['\"]([^'\"]*)['\"]", re.M)
try:
    verstrline = open(VERSIONFILE, "rt").read()
except EnvironmentError:
    pass # Okay, there is no version file.
else:
    mo = VSRE.search(verstrline)
    if mo:
        verstr = mo.group(1)
    else:
        print "unable to find version in %s" % (VERSIONFILE,)
        raise RuntimeError("If %s.py exists, it is required to be well-formed." % (VERSIONFILE,))

setup_requires = []

# darcsver is needed only if you want "./setup.py darcsver" to write a new
# version stamp in dupfilefind/_version.py, with a version number derived from
# darcs history.  http://pypi.python.org/pypi/darcsver
if "darcsver" in sys.argv[1:]:
    setup_requires.append('darcsver >= 1.0.0')

# setuptools_darcs is required to produce complete distributions (such as with
# "sdist" or "bdist_egg"), unless there is a dupfilefind.egg-info/SOURCE.txt file
# present which contains a complete list of files that should be included.
# http://pypi.python.org/pypi/setuptools_darcs
setup_requires.append('setuptools_darcs >= 1.1.0')

install_requires=["argparse >= 0.8", "pyutil >= 1.3.26"],
try:
    import bsddb
except ImportError:
    # If this Python Standard Library doesn't come with an importable bsddb, then we require the bsddb3 distribution.
    install_requires.append("bsddb3")

setup(name='dupfilefind',
      version=verstr,
      description='find files with identical contents, or print out a list of all files and their md5 sums and sizes',
      long_description=open('README.txt', 'rU').read(),
      author='Zooko O\'Whielacronx',
      author_email='zooko@zooko.com',
      url='http://tahoe-lafs.org/trac/dupfilefind',
      license='GPL',
      install_requires=install_requires,
      packages=find_packages(),
      include_package_data=True,
      setup_requires=setup_requires,
      classifiers=trove_classifiers,
      entry_points = { 'console_scripts': [ 'dupfilefind = dupfilefind.cmdline_dupfilefind:main'] },
      zip_safe=False, # I prefer unzipped for easier access.
      )
