About
-----

hghudson provides you a way to perform integration between Mercurial and
Hudson CI Server.

Installation
------------

Install from sources::

        $ python setup.py install

Or from Pypi::

        $ easy_install -U hghudson

Using it
--------

::

  [hudson]
  url=localhost:8080
  job=Foo

  [hooks]
  pretxnchangegroup.build=python:hghudson.build

This is the code you should put in your .hg/hgrc file, and you should configure
Hudson for allowing builds from a trigger.

Be sure the hook code is in the PYTHONPATH environment variable.

To Do
-----
- Allow to build into a secured Hudson
