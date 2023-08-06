Changelog
=========

1.0.0 (2010-10-29)
------------------

New
~~~

- New ``.aslocal`` and ``.strftime_local()`` shortcuts in ``Time``
  object. [Valentin Lab]

Changes
~~~~~~~

- Renamed ``INSTALL`` and ``README`` to ``<name>.rst`` for github.
  [Valentin Lab]

- Prepare for ``autogen.sh`` pre-release script. [Valentin Lab]

- Added a small doc on the ``Clock.wait()`` method. [Valentin Lab]

- Moved all docs into docs/source, written a full overview, updated conf
  and changelog. [Valentin Lab]

- Prepared ``setup.py`` for release on github and pypi. [Valentin Lab]

- More doc, better doc. [Valentin Lab]

- Added a default ``repr`` for System and Test ``TimeZone`` objects.
  [Valentin Lab]

- Removed dependency towards ``sact.test``. [Valentin Lab]

0.6.0 (2010-09-17)
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

0.5.0 (2010-07-27)
------------------

Fix
~~~

- Round_date now rounds microseconds as well as seconds. [Pascal Varet]

- Updated package repository URL. [Pascal Varet]

0.4.0 (2010-06-03)
------------------

- Compute the version of the package using current date instead of the
  Mercurial revision. [Jonathan Ballet]

- Package is now versioned with the current date instead of the current
  Mercurial revision. [Jonathan Ballet]

0.3.0 (2010-03-09)
------------------

- Add a default manageable clock (for tests). [Guillaume (GS) Savary]

- Change the Time object human representation. [Guillaume (GS) Savary]

0.2.0 (2010-02-11)
------------------

- Add method to show a local time without time zone. [Guillaume (GS)
  Savary]


