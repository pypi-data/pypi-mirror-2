Changelog
=========

1.0.2 (2011-06-23)
------------------

Changes
~~~~~~~

- Update Buildout to 1.5.2. [Sébastien Douche]

- Updated ``buildout`` part ``doc`` so our ``docs`` directory layout
  remains compatible with ``collective.sphinx.recipe`` 1.0.7. [Valentin
  Lab]

Fix
~~~

- Some date and time methods failed on already instancied ``datetime``.
  [Guillaume Savary]

Other
~~~~~

- Pkg: dev: minor and fixup to ``autogen.sh`` script. [Valentin Lab]

1.0.1 (2011-04-08)
------------------

Changes
~~~~~~~

- Some minor rephrasing in the documentation. [Valentin Lab]

Fix
~~~

- Minor packaging fixups, filled the description field for PyPI,
  corrected the licence, and remove a utf-8 char in the doc that was
  crashing ``python setup.py`` commands. [Valentin Lab]

1.0.0 (2011-04-08)
------------------

New
~~~

- New ``.aslocal`` and ``.strftime_local()`` shortcuts in ``Time``
  object. [Valentin Lab]

Changes
~~~~~~~

- Renamed ``INSTALL`` and ``README`` to ``<name>.rst`` for github.
  [Valentin Lab]

- ``buildout.cfg`` and ``bootstrap.py`` is cleaned from local
  configuration. [Valentin Lab]

- Prepare for ``autogen.sh`` pre-release script. [Valentin Lab]

- Added a small doc on the ``Clock.wait()`` method. [Valentin Lab]

- Moved all docs into docs/source, written a full overview, updated conf
  and changelog. [Valentin Lab]

- Prepared ``setup.py`` for release on github and pypi. [Valentin Lab]

- More doc, better doc. [Valentin Lab]

- Added a default ``repr`` for System and Test ``TimeZone`` objects.
  [Valentin Lab]

- Removed dependency towards ``sact.test``. [Valentin Lab]

0.6.0 (2010-10-29)
------------------

Fix
~~~

- Make tests about time more stable. [Jonathan Ballet]

  This test was asserting that two consecutives calls of the `ts`
  property return different result, the first call being lower than the
  second call.  But the value returned by `ts` is a floating point
  number expressed in seconds, and it seems that, sometimes, Python's so
  fast that the assertion fails. Using the `test` command with `--repeat
  1000`, it seems that I have 2% runs which are failing with this test
  on my computer.  The fix should be sufficient, since each doctest
  lines are reinterpreted by Doctest, and I guess it should have a
  sufficient cost so that it now passes at 100%.

0.5.0 (2010-09-17)
------------------

Fix
~~~

- Round_date now rounds microseconds as well as seconds. [Pascal Varet]

- Updated package repository URL. [Pascal Varet]

0.4.0 (2010-07-27)
------------------

- Compute the version of the package using current date instead of the
  Mercurial revision. [Jonathan Ballet]

- Package is now versioned with the current date instead of the current
  Mercurial revision. [Jonathan Ballet]

0.3.0 (2010-06-03)
------------------

- Add a default manageable clock (for tests). [Guillaume (GS) Savary]

- Change the Time object human representation. [Guillaume (GS) Savary]

- Uniformisation of buildout.cfg. [Valentin Lab]

0.2.0 (2010-03-09)
------------------

- Add method to show a local time without time zone. [Guillaume (GS)
  Savary]

0.1.0 (2010-02-11)
------------------

- Api: __add__ and __sub__ method in Time(). [Guillaume (GS) Savary]

- Add a timestamp property to the Time object. [Guillaume (GS) Savary]

- Time object now inherits from datetime object. [Jonathan Ballet]

- Some more static method to Time object for convenience. [Valentin Lab]

- New function to help convertion towards UTC ts. [Valentin Lab]

- New time/clock lib. [Valentin Lab]


