# Copyright (C) 2013-2016 by Clearcode <http://clearcode.cc>
# and associates (see AUTHORS).

# This file is part of pytest-elasticsearch.

# pytest-elasticsearch is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# pytest-elasticsearch is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with pytest-elasticsearch.  If not, see <http://www.gnu.org/licenses/>.
"""Fixture factories."""
import os.path
import shutil
from tempfile import gettempdir

import pytest
from elasticsearch import Elasticsearch

from pytest_elasticsearch.executor import ElasticSearchExecutor
from pytest_elasticsearch.port import get_port


def return_config(request):
    """Return a dictionary with config options."""
    config = {}
    options = [
        'port', 'transport_tcp_port', 'host', 'cluster_name',
        'network_publish_host',
        'index_store_type', 'logs_prefix', 'logsdir', 'configuration_path'
    ]
    for option in options:
        option_name = 'elasticsearch_' + option
        conf = request.config.getoption(option_name) or \
            request.config.getini(option_name)
        config[option] = conf
    return config


def elasticsearch_proc(executable='/usr/share/elasticsearch/bin/elasticsearch',
                       host=None, port=-1, transport_tcp_port=None,
                       cluster_name=None, network_publish_host=None,
                       index_store_type=None, logs_prefix=None,
                       elasticsearch_logsdir=None,
                       configuration_path='/etc/elasticsearch'):
    """
    Create elasticsearch process fixture.

    .. warning::

        This fixture requires at least version 1.0 of elasticsearch to work.

    :param str executable: elasticsearch's executable
    :param str host: host that the instance listens on
    :param str|int|tuple|set|list port:
        exact port (e.g. '8000', 8000)
        randomly selected port (None) - any random available port
        [(2000,3000)] or (2000,3000) - random available port from a given range
        [{4002,4003}] or {4002,4003} - random of 4002 or 4003 ports
        [(2000,3000), {4002,4003}] -random of given range and set
    :param str cluster_name: name of a cluser this node should work on.
        Used for autodiscovery. By default each node is in it's own cluser.
    :param str network_publish_host: host to publish itself within cluser
        http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/modules-network.html
    :param str index_store_type: index.store.type setting. *memory* by default
        to speed up tests
    :param str logs_prefix: prefix for log filename
    :param str elasticsearch_logsdir: path for logs.
    :param elasticsearch_logsdir: path for elasticsearch logs
    """

    @pytest.fixture(scope='session')
    def elasticsearch_proc_fixture(request):
        """Elasticsearch process starting fixture."""
        config = return_config(request)
        elasticsearch_host = host or config['host']

        elasticsearch_port = get_port(port) or get_port(config['port'])
        elasticsearch_transport_port = get_port(transport_tcp_port) or \
            get_port(config['transport_tcp_port'])

        elasticsearch_cluster_name = \
            cluster_name or config['cluster_name'] or \
            'elasticsearch_cluster_{0}'.format(elasticsearch_port)
        elasticsearch_logs_prefix = logs_prefix or config['logs_prefix']
        elasticsearch_index_store_type = index_store_type or \
            config['index_store_type']
        elasticsearch_network_publish_host = network_publish_host or \
            config['network_publish_host']

        logsdir = elasticsearch_logsdir or config['logsdir']
        logs_path = os.path.join(
            logsdir, '{prefix}elasticsearch_{port}_logs'.format(
                prefix=elasticsearch_logs_prefix,
                port=elasticsearch_port
            ))

        pidfile = os.path.join(
            gettempdir(), 'elasticsearch.{0}.pid'.format(elasticsearch_port))
        work_path = os.path.join(
            gettempdir(), 'elasticsearch_{0}_tmp'.format(elasticsearch_port))
        conf_path = configuration_path or config['configuration_path']

        elasticsearch_executor = ElasticSearchExecutor(
            executable,
            elasticsearch_host,
            elasticsearch_port,
            elasticsearch_transport_port,
            pidfile,
            conf_path,
            logs_path,
            work_path,
            elasticsearch_cluster_name,
            elasticsearch_network_publish_host,
            elasticsearch_index_store_type,
            timeout=60,
        )

        with elasticsearch_executor:
            yield elasticsearch_executor
        shutil.rmtree(work_path)
        shutil.rmtree(logs_path)

    return elasticsearch_proc_fixture


def elasticsearch(process_fixture_name):
    """
    Create Elasticsearch client fixture.

    :param str process_fixture_name: elasticsearch process fixture name
    """
    @pytest.fixture
    def elasticsearch_fixture(request):
        """Elasticsearch client fixture."""
        process = request.getfixturevalue(process_fixture_name)
        if not process.running():
            process.start()

        hosts = '{0!s}:{1!s}'.format(process.host, process.port)

        client = Elasticsearch(hosts=hosts)

        def drop_indexes():
            client.indices.delete(index='*')

        request.addfinalizer(drop_indexes)

        return client

    return elasticsearch_fixture
