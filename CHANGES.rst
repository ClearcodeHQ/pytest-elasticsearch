CHANGELOG
=========

3.0.0
----------

Features
++++++++

- Import FixtureRequest from pytest, not private _pytest.
  Require at least pytest 6.2
- Replace tmpdir_factory with tmp_path_factory

Removals
++++++++


- Removed `logs_prefix` process fixture parameter, `--elasticsearch-logsdir`
  command parameter and `elasticsearch_logsdir` ini configuration option
- Removed `elasticsearch_logsdir` process fixture parameter `--elasticsearch-logs-prefix`
  command parameter and `elasticsearch_logs_prefix` ini configuration option

Support
+++++++

- support only elasticsearch 6.x and up, same as the most recent elasticsearch library

Misc
++++

- rely on `get_port` functionality delivered by `port_for`

2.1.0
----------

Features
++++++++

- Add command line and ini configuration option for the executable.
- Require python 3.7 and up
- Unify handling of a temporary directory, now temporary directory holding logs,
  workdir, pid will be named after fixture name.

Deprecations
++++++++++++

- Deprecated `logs_prefix` process fixture parameter, `--elasticsearch-logsdir`
  command parameter and `elasticsearch_logsdir` ini configuration option
- Deprecated `elasticsearch_logsdir` process fixture parameter `--elasticsearch-logs-prefix`
  command parameter and `elasticsearch_logs_prefix` ini configuration option

Bugfix
++++++

- Handle properly elasticsearch versions with two-digit minor version

Misc
++++

- Migrated CI/CD to Github Actions
- Blackified Codebase

2.0.1
-------

- [cleanup] Drop support for python versions older than 3.6
- [fix] Adjust for mirakuru 2.2.0 and up


2.0.0
-------

- [enhancement] Created a specified Executor to manage elasticsearch
- [enhancement] added new elasticsearch_nooproc fixture to connect to already
  existing elasticsearch index
- [cleanup] Drop support for unused discovery_zen_ping_multicast
  and elasticsearch_configuration_path option
- [cleanup] Drop support for elasticsearch older than 5
- [cleanup] Drop support for python versions older than 3.5
- [bugfix] changed default index.memory type to mmapfs, over long invalid
  memory type

1.3.0
-------

- [feature] - Support for major elasticsearch versions


1.2.1
-------

- [cleanup] - removed path.py dependency

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
