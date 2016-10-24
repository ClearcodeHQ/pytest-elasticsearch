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

.. image:: https://travis-ci.org/ClearcodeHQ/pytest-elasticsearch.svg?branch=v1.2.0
    :target: https://travis-ci.org/ClearcodeHQ/pytest-elasticsearch
    :alt: Tests

.. image:: https://coveralls.io/repos/ClearcodeHQ/pytest-elasticsearch/badge.png?branch=v1.2.0
    :target: https://coveralls.io/r/ClearcodeHQ/pytest-elasticsearch?branch=v1.2.0
    :alt: Coverage Status

.. image:: https://requires.io/github/ClearcodeHQ/pytest-elasticsearch/requirements.svg?tag=v1.2.0
     :target: https://requires.io/github/ClearcodeHQ/pytest-elasticsearch/requirements/?tag=v1.2.0
     :alt: Requirements Status

What is this?
=============

This is a pytest plugin, that enables you to test your code that relies on a running Elasticsearch search engine.
It allows you to specify fixtures for Elasticsearch process and client.

How to use
==========

.. warning::

    This fixture requires at least version 1.0 of elasticsearch to work.

Plugin contains two fixtures

* **elasticsearch** - it's a client fixture that has functional scope, and which cleans Elasticsearch at the end of each test.
* **elasticsearch_proc** - session scoped fixture, that starts Elasticsearch instance at it's first use and stops at the end of the tests.

Simply include one of these fixtures into your tests fixture list.

You can also create additional elasticsearch client and process fixtures if you'd need to:


.. code-block:: python

    from pytest_elasticsearch import factories

    elasticsearch_my_proc = factories.elasticsearch_proc(
        port=None, logsdir='/tmp')
    elasticsearch_my = factories.elasticsearch('elasticsearch_my_proc')

.. note::

    Each elasticsearch process fixture can be configured in a different way than the others through the fixture factory arguments.

Configuration
=============

You can define your settings in three ways, it's fixture factory argument, command line option and pytest.ini configuration option.
You can pick which you prefer, but remember that these settings are handled in the following order:

    * ``Fixture factory argument``
    * ``Command line option``
    * ``Configuration option in your pytest.ini file``

+----------------------+--------------------------------------+------------------------------------------------------+----------------------------------------------------+------------------------------+
| Elasticsearch option | Fixture factory argument             | Command line option                                  | pytest.ini option                                  | Default                      |
+======================+======================================+======================================================+====================================================+==============================+
| logs directory       | logsdir                              | --elasticsearch-logsdir                              | elasticsearch_logsdir                              | $TMPDIR                      |
+----------------------+--------------------------------------+------------------------------------------------------+----------------------------------------------------+------------------------------+
| host                 | host                                 | --elasticsearch-host                                 | elasticsearch_host                                 | 127.0.0.1                    |
+----------------------+--------------------------------------+------------------------------------------------------+----------------------------------------------------+------------------------------+
| port                 | port                                 | --elasticsearch-port                                 | elasticsearch_port                                 | random                       |
+----------------------+--------------------------------------+------------------------------------------------------+----------------------------------------------------+------------------------------+
| cluster_name         | cluster_name                         | --elasticsearch-cluster-name                         | elasticsearch_cluster_name                         | elasticsearch_cluster_<port> |
+----------------------+--------------------------------------+------------------------------------------------------+----------------------------------------------------+------------------------------+
| index store type     | index_store_type                     | --elasticsearch-index-store-type                     | elasticsearch_index_store_type                     | memory                       |
+----------------------+--------------------------------------+------------------------------------------------------+----------------------------------------------------+------------------------------+
| network publish host | network_publish_host                 | --elasticsearch-network-publish-host                 | elasticsearch_network_publish_host                 | 127.0.0.1                    |
+----------------------+--------------------------------------+------------------------------------------------------+----------------------------------------------------+------------------------------+
| logs prefix          | logs_prefix                          | --elasticsearch-logs-prefix                          | elasticsearch_logs_prefix                          |                              |
+----------------------+--------------------------------------+------------------------------------------------------+----------------------------------------------------+------------------------------+
| enable zen discovery | discovery_zen_ping_multicast_enabled | --elasticsearch-discovery-zen-ping-multicast-enabled | elasticsearch_discovery_zen_ping_multicast_enabled | False                        |
+----------------------+--------------------------------------+------------------------------------------------------+----------------------------------------------------+------------------------------+

Example usage:

* pass it as an argument in your own fixture

    .. code-block:: python

        elasticsearch_proc = factories.elasticsearch_proc(
            cluster_name='awsome_cluster)

* use ``--elasticsearch-logsdir`` command line option when you run your tests

    .. code-block::

        py.test tests --elasticsearch-cluster-name=awsome_cluster


* specify your directory as ``elasticsearch_cluster_name`` in your ``pytest.ini`` file.

    To do so, put a line like the following under the ``[pytest]`` section of your ``pytest.ini``:

    .. code-block:: ini

        [pytest]
        elasticsearch_cluster_name = awsome_cluster

Package resources
-----------------

* Bug tracker: https://github.com/ClearcodeHQ/pytest-elasticsearch/issues
