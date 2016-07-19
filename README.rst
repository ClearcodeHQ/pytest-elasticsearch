pytest-elasticsearch
====================

.. image:: https://img.shields.io/pypi/v/pytest-elasticsearch.svg
    :target: https://pypi.python.org/pypi/pytest-elasticsearch/
    :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/wheel/pytest-elasticsearch.svg
    :target: https://pypi.python.org/pypi/pytest-elasticsearch/
    :alt: Wheel Status

.. image:: https://img.shields.io/pypi/pyversions/pytest-elasticsearch.svg
    :target: https://pypi.python.org/pypi/pytest-elasticsearch/
    :alt: Supported Python Versions

.. image:: https://img.shields.io/pypi/l/pytest-elasticsearch.svg
    :target: https://pypi.python.org/pypi/pytest-elasticsearch/
    :alt: License

Package status
--------------

.. image:: https://travis-ci.org/ClearcodeHQ/pytest-elasticsearch.svg?branch=v0.0.0
    :target: https://travis-ci.org/ClearcodeHQ/pytest-elasticsearch
    :alt: Tests

.. image:: https://coveralls.io/repos/ClearcodeHQ/pytest-elasticsearch/badge.png?branch=v0.0.0
    :target: https://coveralls.io/r/ClearcodeHQ/pytest-elasticsearch?branch=v0.0.0
    :alt: Coverage Status

.. image:: https://requires.io/github/ClearcodeHQ/pytest-elasticsearch/requirements.svg?tag=v0.0.0
     :target: https://requires.io/github/ClearcodeHQ/pytest-elasticsearch/requirements/?tag=v0.0.0
     :alt: Requirements Status

What is this?
=============

This is a pytest plugin, that enables you test your code that relies on an Elasticsearch search engine.
It allows you to specify fixtures for Elasticsearch process and client.

How to use
==========

``Warning`` This fixture requires at least version 1.0 of elasticsearch to work.

You can set and run elasticsearch process with your own settings (i.e. use random port or define your own logsdir)

.. code-block:: 
    elasticsearch_proc = factories.elasticsearch_proc(
        port='?', logsdir='/tmp')

You can use elasticsearch client fixture to run your test. (Remember that client fixture requires a process fixture to work properly.)

.. code-block::
    elasticsearch = factories.elasticsearch(elasticsearch_proc)

To check if everything is ready to go, you can always test both fixtures:

    .. code-block::
        def test_elastic_process(elasticsearch_proc):
            """Simple test for starting elasticsearch_proc."""
            assert elasticsearch_proc.running() is True


        def test_elasticsarch(elasticsearch):
            """Tests if elasticsearch fixtures connects to process."""

            info = elasticsearch.info()
            assert info['status'] == 200

Configuration
=============

You can define your own path for elasticsearch logs directory. There are three ways to achieve this:

* pass it as an argument in your own fixture

    .. code-block:: fixture
        elasticsearch_proc = factories.elasticsearch_proc(
            logsdir='/tmp')

* use ``--elasticsearch-logsdir`` command line option when you run your tests

    .. code-block:: command_line
        py.test tests --elasticsearch-logsdir=/tmp


* specify your directory as ``logsdir`` in your ``pytest.ini`` file.

    To do so, put a line like the following under the ``[pytest]`` section of your ``pytest.ini``:

    .. code-block:: ini

        [pytest]
        elasticsearch_logsdir =
          /tmp/elasticsearch/logs

If you don't want to define your own directory path in any given way, you can always use a default value,
which is simply ``/tmp``. If you do, you have to remember about the order of priority: 

    * ``fixture argument``
    * ``--elasticsearch-logsdir``
    * ``logsdir in pytest.ini``


Package resources
-----------------

* Bug tracker: https://github.com/ClearcodeHQ/pytest_elasticsearch/issues
* Documentation: http://pytest_elasticsearch.readthedocs.org/


Travis-ci
---------

After creating package on github, move to tracis-ci.org, and turn on ci builds for given package.
