
=====
alart
=====

alart is a pseudo-random art generator. It generates
silhouettes. Example images can be found online on
http://metanohi.org/projects/alart/images/


License
=======

alart is free software under the terms of the GNU General Public
License version 3 (or any later version). This is version 0.1.0
(codename: "Ablaze") of the program.


Installing
==========

Way #1
------

Just run this (requires that you have python-pip or python-setuptools
installed)::

  # pip install alart

or::

  # easy_install alart


Way #2
------

Get the newest version of alart at http://metanohi.org/projects/alart/
or at http://pypi.python.org/pypi/alart

Extract the downloaded file and run this in a terminal::

  # python setup.py install

  
Dependencies
============

Python 2.5 is required, though newer versions might be needed for
Encapsulated PostScript support.

alart depends on cairo and cairo's Python bindings for generating
images. Version 1.6 is needed for best output support, but earlier
versions (e.g. 1.4) works ok. To install it, do one of these things:

* For DEB-based distros (Debian etc.): type ``apt-get install python-cairo``
* For RPM-based distros (Fedora etc.): type ``yum install pycairo``
* For other distros: do something similar or get it at
  http://cairographics.org/download/

alart depends on PyGame 1.8.0+ (perhaps earlier versions are also
supported) for showing generated images. If you only want to generate
images, not show them in an interactive window, you do not need PyGame
graphics and sound. To install it, do one of these things:

* For DEB-based distros (Debian etc.): type ``apt-get install python-pygame``
* For RPM-based distros (Fedora etc.): type ``yum install pygame``
* For other distros: do something similar or get it at
  http://pygame.org/download.shtml


Using
=====

To use alart, just run ``alart``. This will display a generated image
with default options. To generate a new image while in the window,
press R.

To see a list of alart's command-line options with explanations, run
``alart --help``. To see alart's module help, run ``pydoc
alart``. Example programs using alart as a module can be found in the
``examples`` directory.


Developing
==========

alart is written in Python and uses Git for branches. To get the
latest branch, get it from gitorious.org like this::

  $ git clone git://gitorious.org/alart/alart.git

Bugs can be reported at ns@metanohi.org (address of sole developer)


This document
=============

Copyright (C) 2010  Niels Serup

Copying and distribution of this file, with or without modification,
are permitted in any medium without royalty provided the copyright
notice and this notice are preserved.  This file is offered as-is,
without any warranty.

