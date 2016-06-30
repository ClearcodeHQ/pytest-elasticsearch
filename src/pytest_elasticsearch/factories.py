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
import shutil

import pytest
from path import path

from elasticsearch import Elasticsearch
from mirakuru import HTTPExecutor
from pytest_elasticsearch.port import get_port


def elasticsearch_proc(executable='/usr/share/elasticsearch/bin/elasticsearch',
                       host='127.0.0.1', port=9201, cluster_name=None,
                       network_publish_host='127.0.0.1',
                       discovery_zen_ping_multicast_enabled=False,
                       index_store_type='memory', logs_prefix=''):
    """
    Create elasticsearch process fixture.

    .. warning::

        This fixture requires at least version 1.0 of elasticsearch to work.

    :param str executable: elasticsearch's executable
    :param str host: host that the instance listens on
    :param int|str port: exact port that the instance listens on (e.g. 8000),
        or randomly selected port:
            '?' - any random available port
            '2000-3000' - random available port from a given range
            '4002,4003' - random of 4002 or 4003 ports
    :param str cluster_name: name of a cluser this node should work on.
        Used for autodiscovery. By default each node is in it's own cluser.
    :param str network_publish_host: host to publish itself within cluser
        http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/modules-network.html
    :param bool discovery_zen_ping_multicast_enabled: whether to enable or
        disable host discovery
        http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/modules-discovery-zen.html
    :param str index_store_type: index.store.type setting. *memory* by default
        to speed up tests
    :param str logs_prefix: prefix for log filename
    """
    @pytest.fixture(scope='session')
    def elasticsearch_proc_fixture(request):
        """Elasticsearch process starting fixture."""
        elasticsearch_port = get_port(port)

        pidfile = '/tmp/elasticsearch.{0}.pid'.format(elasticsearch_port)
        home_path = '/tmp/elasticsearch_{0}'.format(elasticsearch_port)
        logsdir = path(request.config.getvalue('logsdir'))
        logs_path = logsdir / '{prefix}elasticsearch_{port}_logs'.format(
            prefix=logs_prefix,
            port=elasticsearch_port
        )
        work_path = '/tmp/elasticsearch_{0}_tmp'.format(elasticsearch_port)
        cluster = cluster_name or 'dbfixtures.{0}'.format(elasticsearch_port)
        multicast_enabled = str(discovery_zen_ping_multicast_enabled).lower()

        command_exec = '''
            {deamon} -p {pidfile} --http.port={port}
            --path.home={home_path}  --default.path.logs={logs_path}
            --default.path.work={work_path}
            --default.path.conf=/etc/elasticsearch
            --cluster.name={cluster}
            --network.publish_host='{network_publish_host}'
            --discovery.zen.ping.multicast.enabled={multicast_enabled}
            --index.store.type={index_store_type}
            '''.format(
            deamon=executable,
            pidfile=pidfile,
            port=elasticsearch_port,
            home_path=home_path,
            logs_path=logs_path,
            work_path=work_path,
            cluster=cluster,
            network_publish_host=network_publish_host,
            multicast_enabled=multicast_enabled,
            index_store_type=index_store_type

        )

        elasticsearch_executor = HTTPExecutor(
            command_exec, 'http://{host}:{port}'.format(
                host=host,
                port=elasticsearch_port
            ),
            timeout=60,
        )

        elasticsearch_executor.start()

        def finalize_elasticsearch():
            elasticsearch_executor.stop()
            shutil.rmtree(home_path)

        request.addfinalizer(finalize_elasticsearch)
        return elasticsearch_executor

    return elasticsearch_proc_fixture


def elasticsearch(process_fixture_name):
    """
    Create Elasticsearch client fixture.

    :param str process_fixture_name: elasticsearch process fixture name
    """
    @pytest.fixture
    def elasticsearch_fixture(request):
        """Elasticsearch client fixture."""
        process = request.getfuncargvalue(process_fixture_name)
        if not process.running():
            process.start()

        hosts = '{0!s}:{1!s}'.format(process.host, process.port)

        client = Elasticsearch(hosts=hosts)

        def drop_indexes():
            client.indices.delete(index='*')

        request.addfinalizer(drop_indexes)

        return client

    return elasticsearch_fixture
