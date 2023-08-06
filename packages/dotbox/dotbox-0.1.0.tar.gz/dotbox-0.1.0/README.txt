
======
DotBox
======

DotBox is a block-based game mini library. It greatly limits what is
plausible.


License
=======

DotBox is free software under the terms of the GNU General Public
License version 3 (or any later version). The author of DotBox is
Niels Serup, contactable at ns@metanohi.org. This is version 0.1.0 of
the program.

All libraries used by DotBox are GPL-compatible. Any data used by the
examples included in this package is as free as DotBox itself.


Installing
==========

Way #1
------
Just run this (requires that you have python-setuptools installed)::

  $ sudo easy_install dotbox

Way #2
------
Get the newest version of DotBox at
http://metanohi.org/projects/dotbox/ or at
http://pypi.python.org/pypi/dotbox

Extract the downloaded file and run this in a terminal::

  # python setup.py install

Dependencies
============

DotBox should work with both Python 2.6+ and Python 3.x.

DotBox depends on PyGame 1.8.1+ (perhaps earlier versions are also
supported, though at least version 1.9.0 is needed for Python 3).

* For DEB-based distros (Debian etc.): type ``apt-get install python-pygame``
* For RPM-based distros (Fedora etc.): type ``yum install pygame``
* For other distros: do something similar or get it at
  http://pygame.org/download.shtml


Using
=====

DotBox is a mini library with little functionality. Its documentation
is included in its source code, so you can run this command to find
out more about it (as this /is/ a 0.1.0 release, not much is shown
yet; to figure out how to use DotBox, take a look the included
examples instead)::

  $ pydoc dotbox


Example games
-------------

Instead of the lacking documentation, you can also take a look at the
example games in the ``examples`` directory of this package. These
games are playable.


Usable colors
-------------

DotBox uses a palette of 256 colors. The first 216 are the so-called
"web-safe" colors (see
http://en.wikipedia.org/wiki/Web-safe_color#Color_table ), while the
remaining 40 are grayscale.


Developing
==========

DotBox is written in Python and uses Git for branches. To get the
latest branch, get it from gitorious.org like this::

  $ git clone git://gitorious.org/dotbox/dotbox.git


This document
=============

Copyright (C) 2011  Niels Serup

Copying and distribution of this file, with or without modification,
are permitted in any medium without royalty provided the copyright
notice and this notice are preserved.  This file is offered as-is,
without any warranty.
