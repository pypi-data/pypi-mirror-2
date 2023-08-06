=============
Simple Random
=============

:Author: Craig McQueen
:Contact: http://craig.mcqueen.id.au/
:Copyright: 2010 Craig McQueen


Simple pseudo-random number generators, from George Marsaglia.

-----
Intro
-----

The ``simplerandom`` package is provided, which contains modules containing
classes for various simple pseudo-random number generators.

One module provides Python iterators, which generate simple unsigned 32-bit
integers identical to their C counterparts.

Another module provides random classes that are sub-classed from the class
``Random`` in the ``random`` module of the standard Python library.

Why use this package? These random number generators are very simple, which
has two main advantages:

* It is easy to port them to a different platform and/or language. It can be
  useful to be able to implement the identical algorithm on multiple
  platforms and/or languages.
* Small and simple generators can be more appropriate for small embedded
  systems, with limited RAM and ROM.

An equivalent C implementation (of the Python ``simplerandom.iterators``
module) has been created. See:

    http://bitbucket.org/cmcqueen1975/simplerandom

Algorithms
``````````

The algorithms were obtained from two newsgroup posts by George Marsaglia
[#marsaglia1999]_ [#marsaglia2003]_. However, some modifications have been
made. From [#rose]_, it seems that the SHR3 algorithm defined in
[#marsaglia1999]_ is flawed and should not be used. It doesn't actually have a
period of 2**32-1 as expected, but has 64 different cycles, some with very
short periods. The SHR3 in the 2003 post is very similar, but with two shift
values swapped. My suspicion is that the SHR3 shift values in the 1999 post
are a typo.

We still care about KISS from [#marsaglia1999]_ mainly because it uses 32-bit
calculations for MWC, which can be more suitable for small embedded systems.
So we define KISS that uses the MWC from [#marsaglia1999]_, but the Cong and
SHR3 from [#marsaglia2003]_.


References
``````````

.. [#marsaglia1999] | `Random Numbers for C\: End, at last?`__
                    | George Marsaglia
                    | Newsgroup post, sci.stat.math and others, Thu, 21 Jan 1999

.. __:
.. _Random Numbers for C\: End, at last?:
    http://www.cse.yorku.ca/~oz/marsaglia-rng.html

.. [#marsaglia2003] | `RNGs`__
                    | George Marsaglia
                    | Newsgroup post, sci.math, 26 Feb 2003

.. __:
.. _RNGs:
    http://groups.google.com/group/sci.math/msg/9959175f66dd138f

.. [#rose]      | `KISS: A Bit Too Simple`__
                | Greg Rose
                | Qualcomm Inc.

.. __:
.. _KISS\: A Bit Too Simple:
    http://eprint.iacr.org/2011/007.pdf


----------------
Modules Provided
----------------

==========================  ===========================================================================
Module                      Description
==========================  ===========================================================================
``simplerandom.iterators``  Iterator classes, which generate unsigned 32-bit integers.
``simplerandom.random``     Classes that conform to standard Python ``random.Random`` API.
==========================  ===========================================================================


Random Number Generators Provided
`````````````````````````````````

In ``simplerandom.iterators``, the following pseudo-random number generators are provided:

==========================  ===========================================================================
Generator                   Notes
==========================  ===========================================================================
``RandomMWCIterator``       Two 32-bit MWCs combined. From [#marsaglia1999]_.
``RandomCongIterator``      From [#marsaglia2003]_.
``RandomSHR3Iterator``      From [#marsaglia2003]_.
``RandomLFIB4Iterator``     From [#marsaglia1999]_.
``RandomSWBIterator``       From [#marsaglia1999]_.
``RandomFibIterator``       Not useful on its own, but can be used in a combination with other generators. From [#marsaglia1999]_.
``RandomMWC64Iterator``     A single 64-bit multiply-with-carry calculation. From [#marsaglia2003]_.
``RandomKISSIterator``      Combination of MWC, Cong and SHR3. Based on [#marsaglia1999]_ but using [#marsaglia2003]_ Cong and SHR3.
``RandomKISS2Iterator``     Combination of MWC64, Cong and SHR3. From [#marsaglia2003]_.
==========================  ===========================================================================

In ``simplerandom.random``, the following pseudo-random number generators are provided:

==========================  ===========================================================================
Generator                   Notes
==========================  ===========================================================================
``RandomMWC``               Two 32-bit MWCs combined. From [#marsaglia1999]_.
``RandomCong``              From [#marsaglia2003]_.
``RandomSHR3``              From [#marsaglia2003]_.
``RandomLFIB4``             From [#marsaglia1999]_.
``RandomSWB``               From [#marsaglia1999]_.
``RandomMWC64``             A single 64-bit multiply-with-carry calculation. From [#marsaglia2003]_.
``RandomKISS``              Combination of MWC, Cong and SHR3. Based on [#marsaglia1999]_ but using [#marsaglia2003]_ Cong and SHR3.
``RandomKISS2``             Combination of MWC64, Cong and SHR3. From [#marsaglia2003]_.
==========================  ===========================================================================


-----
Usage
-----

Iterators
`````````

    >>> import simplerandom.iterators as sri
    >>> rng = sri.RandomKISSIterator(123958, 34987243, 3495825239, 2398172431)
    >>> next(rng)
    702895144L
    >>> next(rng)
    13983691L
    >>> next(rng)
    699724563L

Random class API
````````````````

    >>> import simplerandom.random as srr
    >>> rng = srr.RandomKISS(258725234)
    >>> rng.random()
    0.77345210517180141
    >>> rng.random()
    0.27725185740138936
    >>> rng.random()
    0.91217281705021191


-------------------------
Supported Python Versions
-------------------------

Currently this has had basic testing on Ubuntu 10.04 32-bit and
Windows XP 32-bit. It passes the basic ``simplerandom.iterators.test`` unit
tests, as well as basic manual testing of ``simplerandom.random``. A more
thorough unit test suite is needed.

In Ubuntu, it has been tested on Python 2.6 and 3.1 and passes.

In Windows, it has been tested on Python 2.4, 2.5, 2.6, 2.7, 3.1 and 3.2.
It passes under these versions.

The pure Python code is expected to work on 64-bit platforms, but has not been
tested. The Cython version of ``simplerandom.iterators`` should work on 64-bit
platforms, but has not been tested.


-------------
Use of Cython
-------------

`Cython`_ is used to make a fast implementation of ``simplerandom.iterators``.
Cython creates a ``.c`` file that can be compiled into a Python binary
extension module.

The ``simplerandom`` source distribution package includes a ``.c`` file that
was created with Cython, so it is not necessary to have Cython installed to
install ``simplerandom``.

The Cython ``.pyx`` file is also included, if you want to modify the Cython
source code, in which case you do need to have Cython installed. But by
default, ``setup.py`` builds the extension from the ``.c`` file (to ensure
that the build doesn't fail due to particular Cython version issues). If you
wish to build using Cython from the included ``.pyx`` file, you must set
``USE_CYTHON=True`` in ``setup.py``.

.. _Cython:
    http://cython.org/


------------
Installation
------------

The simplerandom package is installed using ``distutils``.  If you have the tools
installed to build a Python extension module, run the following command::

    python setup.py install

If you cannot build the C extension, you may install just the pure Python
implementation, using the following command::

    python setup.py build_py install --skip-build


------------
Unit Testing
------------

Basic unit testing of the iterators is in ``simplerandom.iterators.test``. It
duplicates the tests of the C algorithms given in the original newsgroup post
[#marsaglia1999]_, as well as other unit tests.

To run it on Python >=2.5::

    python -m simplerandom.iterators.test

Alternatively, in the ``test`` directory run::

    python test_iterators.py

A more thorough unit test suite is needed.


-------
License
-------

The code is released under the MIT license. See LICENSE.txt for details.

