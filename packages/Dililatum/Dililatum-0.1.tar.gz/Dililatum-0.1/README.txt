=========
Dililatum
=========

Have you ever heard of Dililatum?

Perhaps not. For Dililatum is Something New. Dililatum has a quest;
and that quest is to distribute Python power to quest-oriented
RPG-like computer-based keyboard-using video games. At least that's
its purpose.

Dililatum can be considered a game engine, but in reality it's a game
library. It is written in Python using PyGame for graphics and sound
in games. Dililatum also depends on NumPy. More specifically, it's
like this:


Dependencies
============

Dililatum depends on the following programs/libraries::

    Python 2.5+
    Dililatum is written in Python
    <http://python.org/>
    Debian etc.: apt-get install python
    Fedora etc.: yum install python

    PyGame 1.8.1+
    Dililatum uses PyGame for its graphics and sound
    <http://python.org/>
    Debian etc.: apt-get install python-pygame
    Fedora etc.: yum install pygame

    NumPy
    Dililatum uses NumPy for internal arrays describing
    where it's okay to walk -- and where it's not ok.
    <http://numpy.scipy.org/>
    Debian etc.: apt-get install python-numpy
    Fedora etc.: yum install python-numpy

Optional modules
----------------

Additionally, you can also install these libraries::
    setproctitle
    Changes 'python' to 'dililatum'
    <http://pypi.python.org/pypi/setproctitle/>
    sudo easy_install setproctitle

    termcolor
    Colors Dililatum's terminal output
    <http://pypi.python.org/pypi/termcolor>
    sudo easy_install termcolor


Details
=======

Dililatum is released under the GNU GPLv3+ and is free
software. Dililatum is downloadable from
http://metanohi.org/projects/dililatum/. The version of this
Dililatum is v0.1. Many features are not complete yet.

For an example of what Dililatum is capable of, try downloading
ForestQuest. It's available at
http://metanohi.org/projects/forestquest/. It's still a work in
progress, but it works.

The logo of Dililatum, found in the "logo" directory, is available
under the terms of the Creative Commons Attribution-ShareAlike 3.0 (or
any later version) Unported license. A copy of this license is
available at http://creativecommons.org/licenses/by-sa/3.0/


Installing
==========

To install Dililatum, write this in a terminal::

    $ ./setup.py install

After installing it, you can run it like this::

    $ dililatum GAME

If you choose not to install it, the Python file you should run is
called "dililatum" and located in the "bin" directory.

Note that Dililatum has many command-line options, which is why it's a
good idea to run "dililatum --help".

Dililatum comes with several tools for more easily developing
games. These are named 'dilatiumdev*'.

Documentation is available in the "docs" directory.

Developers are very welcome.

The original author of Dililatum is Niels Serup <ns@metanohi.org>.
