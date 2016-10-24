CHANGELOG
=========

1.2.0
-------

- [feature] - migrate usage of getfuncargvalue to getfixturevalue. require at least pytest 3.0.0
- [feature] - default logsdir to $TMPDIR
- [feature] - run process on random port by default - enhances xdist experience

1.1.0
-------

- [feature] use tmpfile.gettempdir instead of hardcoded /tmp directory
- [docs] added description to all command line and ini options
- [bugfix] made command line option's dests more distinc, to prevent from influencing other pytest plugins

1.0.0
-------

- [feature] pytest.ini option for every command line option
- [feature] Command line options for every fixture factory argument
- Extracted original code from pytest-dbfixtures
