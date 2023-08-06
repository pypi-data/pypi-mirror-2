==============================
Apptrace for Google App Engine
==============================

The apptrace package provides a WSGI middleware for tracking memory usage in
Google App Engine Python applications.

Since apptrace is meant for development and debugging purposes only, it works
with the development appserver of the Google App Engine Python SDK and
TyphoonAE. It will definitely not work on the GAE production environment.

Copyright and License
---------------------

Copyright 2010, 2011 Tobias Rodaebel

This software is released under the Apache License, Version 2.0. You may obtain
a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Google App Engine is a trademark of Google Inc.

Requirements
------------

The apptrace package requires Guppy-PE (http://guppy-pe.sourceforge.net) to be
installed on your PYTHONPATH. It will be automatically installed when you use
the `easy_install` command.

Installation
------------

The easiest way to install apptrace is (provided that you have setuptools
installed) to use `easy_install apptrace`.

Running Apptrace
----------------

In order to run the demo application with apptrace run following commands::

  $ apptracectl init demo 
  $ python dev_appserver.py demo

See this wiki page for a more detailed documentation on using apptrace:

  http://code.google.com/p/apptrace/wiki/UsingApptrace

Buildout
--------

If you want to tinker with the most recent development version of apptrace,
install the development environment by typing following commands::

  $ hg clone https://apptrace.googlecode.com/hg apptrace-dev
  $ cd apptrace-dev
  $ python bootstrap.py --distribute
  $ ./bin/buildout

Running Unit Tests
------------------

All unit tests can be run by executing the following command::

  $ ./bin/python setup.py test --appengine-path=<path to the SDK>

Contact
-------

Tobias Rodaebel <tobias dot rodaebel at googlemail dot com>
