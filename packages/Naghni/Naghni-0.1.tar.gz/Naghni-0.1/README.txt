======
Naghni
======

Naghni is a simple side-scrolling game. You are a round creature whose
purpose is to fill empty holes with matter, thus closing them. It
matters greatly to your round friends that you do a job well-done,
because if you don’t, they’re all going to die!

If you want to save the naghnies (for that is the name of the people),
you should not hesitate to play Naghni. You will be their Saviour,
their Hope, their Light in the darkest of times.

Naghni levels consist of you and a lot of other objects. At least one
hole is always present. It is your purpose to collect edible objects
and then return those objects to the holes. Holes disappear when they
have had enough to eat. When all holes are gone, the level has been
completed. Holes differ from other objects in that they have borders.

As of now, it's not possible to die. You may however end up in
situations that require a restart.

Naghni is free software under the terms of the GNU General Public
License version 3 (or any later version). The author of Naghni is
Niels Serup, contactable at ns@metanohi.org . This is version 0.1 of
the program. Naghni includes program data created by other people and
under other free licenses; the details can be found in the file
LICENSING.txt.


Installing
==========

Naghni depends on PyGame 1.8.1+ for graphics and sound. To install
PyGame, do one of these things:

* For Debian etc.: type ``apt-get install python-pygame``
* For Fedora etc.: type ``yum install pygame``
* Or get it at http://pygame.org/download.shtml

Naghni also depends on pycairo, NumPy and librsvg.

``apt-get install python-cairo``, or ``yum install pycairo``, or visit
http://cairographics.org/pycairo/

``apt-get install python-numpy``, or ``yum install python-numpy``, or
visit http://numpy.scipy.org/

``apt-get install python-rsvg``, or ``gnome-python2-rsvg``, or
http://librsvg.sourceforge.net/

Optional extras
----------------

If present, Naghni will also use these Python modules:

``setproctitle``
 Web address: http://pypi.python.org/pypi/setproctitle/
   $ sudo easy_install setproctitle

``termcolor``
  Web address: http://pypi.python.org/pypi/termcolor
    $ sudo easy_install termcolor


Way #1
------
Get newest version of Naghni at
http://metanohi.org/projects/naghni/

Extract the downloaded file and run this in a terminal::

  $ sudo python setup.py install

Way #2
------
Just run this (requires that you have python-setuptools installed)::

  $ sudo easy_install naghni


Running
=======

When Naghni has been installed, you can run it from the command-line
like this::

  $ naghni [options]

naghni has several options. Run ``naghni --help`` to see a list of
them. Most of them can also be changed in-game.


Playing
=======

All special aspects of Naghni will (ultimately) be explained
in-game. Do not worry. Use the arrow keys to control your character,
press PageUp/PageDown to zoom in/out and Shift+F to toggle an FPS
viewer. Press the R key to restart a level.


For developers
==============

Naghni uses Git for branches. To get the latest branch, get it from
gitorious.org like this::

  $ git clone git://gitorious.org/naghni/naghni.git

Naghni is written in Python and should be relatively easy to integrate
into other programs (in the future, that is).

Designing levels
----------------
Levels are simply Python files using the Naghni Python files installed
as a mini library. The easy way to create a new level is to modify an
existing level. Such levels can be found in the ``naghnilevels``
directory within the ``data`` directory. No real documentation is
present at this time, and the "API" might change in the future.


The future / TODOs
==================

Naghni currently misses several features.

* It doesn't have a menu.
* It only works with SDL. Creating bindings to OpenGL might be a good
  idea.
* It has only 3 builtin levels, and all of them are test levels,
  i.e. they are not hilariously fun to play.
* There is no story mode. There is barely any story, anyway.
* Characters are boring circles. They should have fancy things on them
  (like eyes, ears, tentacles, etc.).
* It has only 3 builtin patterns. More are needed.
* It lacks real background color/image support.
* It lacks documentation (and a finalized level "format").
* It lacks music and sounds.
* It hasn't been tested thorougly.
* Too few people are playing it.
* There are a few physics-related issues which need to be fixed. It
  would be nice to implement Naghni in a general-purpose physics
  engine instead of its current fault prone one.
* It's slow. Optimization is sadly a must. The more objects a level
  has, the slower it is, partly because of slow loops.
* Code (especially the more complex stuff) isn't explained very well.
* Probably several other things as well.

It will take time to fix this.

The logo
========
The logo of Naghni, found in the "logo" directory, is available
under the terms of the Creative Commons Attribution-ShareAlike 3.0 (or
any later version) Unported license. A copy of this license is
available at http://creativecommons.org/licenses/by-sa/3.0/


This document has been released under the Creative Commons Zero 1.0
Universal license.
