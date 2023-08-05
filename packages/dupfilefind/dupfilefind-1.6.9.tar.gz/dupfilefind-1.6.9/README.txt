===============================
dupfilefind
===============================


Find files with identical contents. Optionally hard-link or delete such files. Works on Windows. Can print out the md5sums and sizes of all your files. Unlike most tools of its ilk, this one will work even if the list of the metadata of all your files is too large to fit into your RAM.

Dupfilefind is reasonably efficient, for what it does. It first compares sizes (so it can tell if files are different) and then inode numbers (so it can tell if different filenames are actually links to the same underlying file contents) before it resorts to computing MD5 sums of file contents. In addition I did some profiling and benchmarking to see how I could make it most efficient, and this is what I came up with.

LICENCE
=======

You may use this package under the GNU General Public License, version 2 or, at your option, any later version.  You may use this package under the Transitive Grace Period Public Licence, version 1.0, or at your option, any later version. (You may choose to use this package under the terms of either licence, at your option.)  See the file `COPYING.GPL`_ for the terms of the GNU General Public License, version 2.  See the file `COPYING.TGPPL.html`_ for the terms of the Transitive Grace Period Public Licence, version 1.0.

See `TGPPL.PDF`_ for why the TGPPL exists, graphically illustrated in four slides.

.. _COPYING.GPL: http://tahoe-lafs.org/trac/dupfilefind/browser/COPYING.GPL
.. _COPYING.TGPPL.html: http://tahoe-lafs.org/source/dupfilefind/trunk/COPYING.TGPPL.html
.. _TGPPL.PDF: http://tahoe-lafs.org/~zooko/tgppl.pdf
