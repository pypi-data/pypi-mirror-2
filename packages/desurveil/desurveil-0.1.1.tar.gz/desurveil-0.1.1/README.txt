
=========
desurveil
=========

desurveil is a cryptography program with support for key pair
generation and encrypting and decrypting with RSA, OAEP, and arbitrary
data lengths.

desurveil is both a command line tool and a Python module. It requires
Python 3.1+.


License
=======

desurveil is free software under the terms of the GNU Affero General
Public License version 3 (or any later version, see file
``COPYING.txt`` or webpage http://gnu.org/licenses/agpl.html for full
license). The author of desurveil is Niels Serup, contactable at
ns@metanohi.org. This is version 0.1.1 of the program.


Installation
============

It is not strictly necessary to install desurveil to use it if you
only plan to use it as a command line tool. It is still recommended,
though. To install it, run::

  python3 setup.py install

You must be a superuser to do this.


Use as command line tool
========================

If you have installed desurveil, run::

  desurveil COMMAND [OPTION]... [INPUT FILE]...

Else, run this::

  python3 scripts/desurveil COMMAND [OPTION]... [INPUT FILE]...

To see how to interact with desurveil, run::

  desurveil --help


Use as Python module
====================

When desurveil has been installed, it can be used just like any other
Python module. To see which functions and classes are available and
usable, run::

  pydoc3 desurveil

And also::

  pydoc3 desurveil.basemath
  pydoc3 desurveil.primes
  pydoc3 desurveil.oaep
  pydoc3 desurveil.keypair
  pydoc3 desurveil.utility

These can be imported with simple ``import`` statements.


Development
===========

Development takes place with Git. To get the latest branch, download
it from gitorious.org::

  $ git clone git://gitorious.org/desurveil/desurveil.git


Logo
====

The logo (``logo.svg``) has been released into the public domain.

  
This document
=============
Copyright (C) 2011 Niels Serup

Copying and distribution of this file, with or without modification,
are permitted in any medium without royalty provided the copyright
notice and this notice are preserved.  This file is offered as-is,
without any warranty.
