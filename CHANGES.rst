CHANGELOG
=========

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
