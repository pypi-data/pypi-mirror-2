Introduction
============

``transmogrify.regexp`` allows you to use regular expressions and format strings
to search and replace key values in a `Transmogrifier`_ pipeline. If your
results are grouped, you may optionally specify a group order.

Installation
============

Sample installation (via `mr.migrator`_)::

    [buildout]
    develop = .
    extends = http://x.aclark.net/plone/4.1.x/develop.cfg
    parts += migrate

    [migrate]
    recipe = mr.migrator
    eggs =
        transmogrify.extract
        transmogrify.filesystem
        transmogrify.ploneremote
        transmogrify.pathsorter
        transmogrify.print
    pipeline = pipeline.cfg


Usage
=====

Sample usage::

    [apply_regexp]
    blueprint = transmogrify.regexp
    key = _path
    expression = /(.*)/(\d\d\d\d)/(\d\d)/(\d\d)/(.+)/index.html
    format = %%s/%%s-%%s%%s%%s.html
    order = 0,4,1,2,3

.. _`mr.migrator`: http://pypi.python.org/pypi/mr.migrator
.. _`Transmogrifier`: http://pypi.python.org/pypi/collective.transmogrifier

