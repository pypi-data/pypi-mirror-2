======================
pycmd scripts
======================

``pycmd`` is a collection of command line tools for helping with Python development.

``py.cleanup``: remove ``.pyc`` and similar files
=============================================================

Usage: ``py.cleanup [PATH]``

Delete pyc file recursively, starting from ``PATH`` (which defaults to the
current working directory). Don't follow links and don't recurse into
directories with a ".".

``py.lookup``: find text in recursively found .py files 
====================================================================

Usage: ``py.lookup SEARCH_STRING [options]``

Looks recursively at Python files for a ``SEARCH_STRING``, starting from the
present working directory. Prints the line, with the filename and line-number
prepended.


``py.countloc``: give LOCs for lines and testlines
=================================================================

Usage: ``py.countloc [PATHS]``

Count (non-empty) lines of python code and number of python files recursively
starting from a ``PATHS`` given on the command line (starting from the current
working directory). Distinguish between test files and normal ones and report
them separately.

``py.which``: print location of an importable package or module
=====================================================================

Usage: ``py.which modulename``

Print the ``__file__`` of the module that is imported via ``import modulename``.
The version-suffix is the same as with ``py.test`` above.

