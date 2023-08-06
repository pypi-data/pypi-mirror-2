createzopecoverage
==================

createzopecoverage provides a ``bin/createzopecoverage`` script that serves as
a one-line coverage report generator.  It is essentially a wrapper around
`z3c.coverage <http://pypi.python.org/pypi/z3c.coverage>`_.  It is intended
for use inside buildouts, so there are two assumptions:

- The directory you run this script from is the root of the buildout.

- There is a ``bin/test``.

And yes, it assumes a z3c.coverage, so a zope test setup.  It doesn't work
with a "regular" coverage.py setup.


Installation and use
--------------------

To install, add ``createzopecoverage`` to a zc.recipe.egg section.  You often
already have one for common scripts.  So something like this::

  [buildout]
  ...
  parts =
      ...
      console_scripts

  [console_scripts]
  recipe = zc.recipe.egg
  eggs =
      ...
      createzopecoverage

alternatively you may use::

  [buildout]
  ...
  parts =
      ...
      createzopecoverage

  [createzopecoverage]
  recipe = createzopecoverage

(Note: you can name your part differently and the binary will be named after
that part).

This gives you a ``bin/createzopecoverage`` script that does the following:

- Check whether bin/test exists.  Safety feature.

- Remove old coverage dir if it exists.  This way you always have clean
  results.

- Run bin/test with the ``--coverage=...`` option.

- Use z3c.coverage to create the actual reports.  By default into
  ``./coverage/reports``.  If you start createzopecoverage with a command line
  argument (``bin/createzopecoverage /tmp/output``) it will put the reports into
  that directory.

- Open the reports in your webbrowser *if you did not specify an output
  directory*.  The assumption here is that if you run the script as-is, you
  just want to see the coverage reports.  If you *do* specify an output
  directory, you're probably running it from within buildbot or so on the
  server and you want the output in some webserver-served directory.  No use
  to open a browser on the server.


Development
-----------

The source code lives at https://bitbucket.org/reinout/createzopecoverage, you
can also `report issues
<https://bitbucket.org/reinout/createzopecoverage/issues>`_ there.  Feel free
to suggest improvements (and especially to make them yourself).


OSX comment
-----------

z3c.coverage uses the "enscript" command for python code highlighting.  The
version provided by OSX before 10.5.7 complains about an unkown ``--footer``
argument passed by z3c.coverage.  There are two possible solutions:

- Update to 10.5.7.  That update came out a few minutes after I wrote this
  original comment :-)

- Install enscript from macports.

- Add a script called "enscript" on your path that calls the original enscript
  minus the offending argument::

    #!/bin/sh
    shift
    /usr/bin/enscript -q --header -h --language=html --color -o - $9


More info
---------

Technical details and a full doctest are in ``createzopecoverage/USAGE.txt``.

Made by `Reinout van Rees <http://reinout.vanrees.org>`_.

Buildout recipe install option made by Michael Howitz.
