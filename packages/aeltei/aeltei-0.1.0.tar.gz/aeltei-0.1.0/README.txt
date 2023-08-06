
======
aeltei
======

aeltei is a virtual multi instrument environment using soundfonts. It allows
one to use a keyboard to enter and play musical notes in a curses interface,
i.e. on the command line. Current limitations include only support for one
channel, no pitch bending, and no saving recordings as MIDI files.

aeltei only works on Python 2.x where x >= 5. Python 3 support would require
Python 3 support in the modules used by this program.


License
=======

aeltei is free software under the terms of the GNU Affero General Public
License version 3 (or any later version). The author of aeltei is Niels Serup,
contactable at ns@metanohi.org (for now, just use this address for bug
reports). This is version 0.1.0 of the program.


Installation
============

To install aeltei the easy way, run::

  easy_install aeltei

(You must be a superuser and have python-setuptools installed to do this.)

Alternatively, you can download aeltei either from
http://metanohi.org/projects/aeltei/ or from http://pypi.python.org/pypi/aeltei
and then install it from the downloaded file. This way you'll also get useful
example files. To install aeltei this way, run::

  python setup.py install

Dependencies
------------

aeltei depends on ``fluidsynth``, ``mingus``, ``pyFluidSynth``, and the
availability of a soundfont (free soundfonts come with ``fluidsynth``).


Use
===

Run ``aeltei --help``.


Development
===========

aeltei uses Git for code management. To get the latest branch, download it from
gitorious.org::

  $ git clone git://gitorious.org/aeltei/aeltei.git



This document
=============
Copyright (C) 2011  Niels Serup

Copying and distribution of this file, with or without modification, are
permitted in any medium without royalty provided the copyright notice and this
notice are preserved.  This file is offered as-is, without any warranty.
