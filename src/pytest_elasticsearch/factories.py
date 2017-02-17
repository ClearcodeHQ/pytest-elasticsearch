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
import errno
import multiprocessing
import os.path
import re
import semver
import shutil
import subprocess
from tempfile import gettempdir

import pytest

from elasticsearch import Elasticsearch
from mirakuru import HTTPExecutor
from pytest_elasticsearch.port import get_port


def _get_elastic_version(executable):
    """Return the Elasticsearch version from executable"""
    # ES 1.x uses '-v' to get the version, while 5.x uses '-V'
    p = subprocess.Popen([executable, "-v -V"], stdout=subprocess.PIPE)
    out, _ = p.communicate()
    if not out.startswith('Version'):   # ES 2.x only knows '--version'
        p = subprocess.Popen([executable, "--version"], stdout=subprocess.PIPE)
        out, _ = p.communicate()

    m = re.match(r'Version: (.+), Build', out)
    return semver.parse_version_info(m.group(1))


def return_config(request):
    """Return a dictionary with config options."""
    config = {}
    options = [
        'port', 'host', 'cluster_name', 'network_publish_host',
        'discovery_zen_ping_multicast_enabled', 'index_store_type',
        'logs_prefix', 'logsdir', 'confdir'
    ]
    for option in options:
        option_name = 'elasticsearch_' + option
        try:
            conf = request.config.getoption(option_name) or \
                   request.config.getini(option_name)
            config[option] = conf
        except ValueError:
            config[option] = None
    return config


def _generate_es_cmdline(es_version, executable, pid_file, **kwargs):
    es_params_to_args = {
        'http.port': 'port',
        'http.host': 'host',
        'default.path.logs': 'logs_path',
        'default.path.conf': 'conf_path',
        'cluster.name': 'cluster',
        'network.publish_host': 'network_publish_host',
        'index.store.type': 'index_store_type'
    }

    if es_version.major < 5:
        es_params_to_args.update({
            'path.home': 'home_path',           # not allowed to change it in 5.x
            'default.path.work': 'work_path',   # doesn't exist in 5.x
            'discovery.zen.ping.multicast.enabled': 'multicast_enabled',
        })

        cmdline_opts = ["--%s=%s" % (es_param, kwargs[arg])
                        for es_param, arg in es_params_to_args.items()
                        if kwargs.get(arg) is not None]
    else:
        es_params_to_args.update({
            'node.max_local_storage_nodes': 'max_local_storage_nodes'
        })

        cmdline_opts = ["-E %s=%s" % (es_param, kwargs[arg])
                        for es_param, arg in es_params_to_args.items()
                        if kwargs.get(arg) is not None]

    return "{daemon} -p {pid_file} {opts}".format(
        daemon=executable,
        pid_file=pid_file,
        opts=' '.join(cmdline_opts)
    )


def _default_index_store(es_version):
    if es_version.major < 2:
        return 'memory'
    else:
        return 'fs'


def _default_conf_dir(es_version):
    if es_version.major == 2:
        return '/etc/elasticsearch'
    else:
        return None


def elasticsearch_proc(executable='elasticsearch',
                       host=None, port=-1, cluster_name=None,
                       network_publish_host=None,
                       discovery_zen_ping_multicast_enabled=None,
                       index_store_type=None, logs_prefix=None,
                       elasticsearch_logsdir=None,
                       elasticsearch_confdir=None):
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
    :param bool discovery_zen_ping_multicast_enabled: whether to enable or
        disable host discovery
        http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/modules-discovery-zen.html
    :param str index_store_type: index.store.type setting. *memory* (ES < 5.0) or *fs* (ES >= 5.0) by default
    :param str logs_prefix: prefix for log filename
    :param str elasticsearch_logsdir: path for logs.
    :param str elasticsearch_confdir: path for Elasticsearch config.
    """

    @pytest.fixture(scope='session')
    def elasticsearch_proc_fixture(request):
        """Elasticsearch process starting fixture."""
        tmpdir = gettempdir()
        config = return_config(request)
        es_ver = _get_elastic_version(executable)

        elasticsearch_host = host or config['host']

        elasticsearch_port = get_port(port) or get_port(config['port'])

        elasticsearch_cluster_name = \
            cluster_name or config['cluster_name'] or \
            'elasticsearch_cluster_{0}'.format(elasticsearch_port)
        elasticsearch_logs_prefix = logs_prefix or config['logs_prefix'] or ''
        elasticsearch_index_store_type = index_store_type or \
                                         config['index_store_type'] or _default_index_store(es_ver)
        elasticsearch_network_publish_host = network_publish_host or \
                                             config['network_publish_host']

        logsdir = elasticsearch_logsdir or config['logsdir'] or tmpdir
        logs_path = os.path.join(
            logsdir, '{prefix}elasticsearch_{port}_logs'.format(
                prefix=elasticsearch_logs_prefix,
                port=elasticsearch_port
            ))

        conf_path = elasticsearch_confdir or config['confdir'] or _default_conf_dir(es_ver)

        pidfile = os.path.join(
            tmpdir, 'elasticsearch.{0}.pid'.format(elasticsearch_port))
        home_path = os.path.join(
            tmpdir, 'elasticsearch_{0}'.format(elasticsearch_port))
        work_path = '{0}_tmp'.format(home_path)

        if discovery_zen_ping_multicast_enabled is not None:
            multicast_enabled = str(
                discovery_zen_ping_multicast_enabled).lower()
        else:
            multicast_enabled = config['discovery_zen_ping_multicast_enabled']

        command_exec = _generate_es_cmdline(
            es_ver, executable=executable, pid_file=pidfile,
            host=elasticsearch_host,
            port=elasticsearch_port,
            home_path=home_path,
            logs_path=logs_path,
            conf_path=conf_path,
            work_path=work_path,
            cluster=elasticsearch_cluster_name,
            network_publish_host=elasticsearch_network_publish_host,
            multicast_enabled=multicast_enabled,
            index_store_type=elasticsearch_index_store_type,
            max_local_storage_nodes=multiprocessing.cpu_count()
        )

        elasticsearch_executor = HTTPExecutor(
            command_exec, 'http://{host}:{port}'.format(
                host=elasticsearch_host,
                port=elasticsearch_port
            ),
            timeout=60
        )

        elasticsearch_executor.start()

        def finalize_elasticsearch():
            elasticsearch_executor.stop()
            try:
                shutil.rmtree(home_path)
            except OSError as e:
                if e.errno != errno.ENOENT:
                    raise

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
