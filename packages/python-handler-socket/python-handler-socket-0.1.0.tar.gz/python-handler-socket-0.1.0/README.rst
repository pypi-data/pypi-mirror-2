====
pyhs
====

Overview
--------

pyhs (python-handler-socket) is a Python client library for the
`HandlerSocket <https://github.com/ahiguti/HandlerSocket-Plugin-for-MySQL/>`_
MySQL plugin.

Installation
------------

First, install MySQL and HandlerSocket

Get the distribution::
    
    pip install python-handler-socket

Or get the package from latest source::

    pip install hg+http://bitbucket.org/excieve/pyhs#egg=python-handler-socket

Or clone the main repository and install manually::

    hg clone http://bitbucket.org/excieve/pyhs
    cd pyhs
    python setup.py install

Check your installation like this::

    python
    >>> from pyhs import __version__
    >>> print __version__

Usage
-----

Usage cases, details and API reference are available
in ``docs`` directory inside the package or
`online <http://python-handler-socket.readthedocs.org/>`_ on RTD.

License
-------

| pyhs is released under MIT license.
| Copyright (c) 2010 Artem Gluvchynsky <excieve@gmail.com>

See ``LICENSE`` file inside the package for full licensing information.
