..   -*- mode: rst -*-

############################
virtualenvwrapper-powershell
############################

A port of Doug Hellmann's virtualenvwrapper for Powershell.

========
Features
========

#.  Organizes all of your virtual environments in one place.

#.  Wrappers for creating, copying and deleting environments, including
    user-configurable hooks.

#.  Use a single command to switch between environments.

.. 4.  Tab completion for commands that take a virtual environment as
..     argument.

#. User-configurable hooks for all operations.

#. Plugin system for more creating sharable extensions.

============
Installation
============

::
	setup.py install

Alternatively, see the `original project documentation
<http://www.doughellmann.com/docs/virtualenvwrapper/>`__ for
guidance on installation and setup.

Supported Shells
================

Powershell 2.0

Python Versions
===============

virtualenvwrapper-powershell is tested under Python 2.7.

=======
Support
=======

Report bugs via the `bug tracker on BitBucket
<http://bitbucket.org/guillermooo/virtualenvwrapper-powershell/>`__.

Shell Aliases
=============

Since virtualenvwrapper is largely a shell script, it uses shell
commands for a lot of its actions.  If your environment makes heavy
use of shell aliases or other customizations, you may encounter
issues.  Before reporting bugs in the bug tracker, please test
*without* your aliases enabled.  If you can identify the alias causing
the problem, that will help make virtualenvwrapper-powershell more robust.

=======
License
=======

Copyright Guillermo López, All Rights Reserved

Permission to use, copy, modify, and distribute this software and its
documentation for any purpose and without fee is hereby granted,
provided that the above copyright notice appear in all copies and that
both that copyright notice and this permission notice appear in
supporting documentation, and that the name of Doug Hellmann not be used
in advertising or publicity pertaining to distribution of the software
without specific, written prior permission.

GUILLERMO LÓPEZ DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO
EVENT SHALL DOUG HELLMANN BE LIABLE FOR ANY SPECIAL, INDIRECT OR
CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF
USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.
