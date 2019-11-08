"""Elasticsearch executor."""

import re
from subprocess import check_output

from mirakuru import HTTPExecutor
from pkg_resources import parse_version


class NoopElasticsearch:  # pylint:disable=too-few-public-methods
    """No operation Elasticsearch executor mock."""

    def __init__(self, host, port):
        """
        Initialize Elasticsearch executor mock
        :param str host: hostname under which elasticsearch is available
        :param int port: port under which elasticsearch is available
        """
        self.host = host
        self.port = port

    @staticmethod
    def running():
        """Mock method pretending the executor is running."""
        return True


# pylint:disable=too-many-instance-attributes
class ElasticSearchExecutor(HTTPExecutor):
    """Elasticsearch executor."""

    def __init__(
            self, executable, host, port, tcp_port,
            pidfile, logs_path, works_path,
            cluster_name, network_publish_host, index_store_type, timeout
    ):   # pylint:disable=too-many-arguments
        """
        Initialize ElasticSearchExecutor.

        :param pathlib.Path executable: Executable path
        :param str host: hostname under which elasticsearch will be running
        :param int port: port elasticsearch listens on
        :param int tcp_port: port used for unternal communication
        :param pathlib.Path pidfile: pidfile location
        :param pathlib.Path logs_path: log files location
        :param pathlib.Path works_path: workdir location
        :param str cluster_name: cluster name
        :param str network_publish_host: network host to which elasticsearch
            publish to connect to cluseter'
        :param str index_store_type: type of the index to use in the
            elasticsearch process fixture
        :param int timeout: Time after which to give up to start elasticsearch
        """
        self._version = None
        self.executable = executable
        self.host = host
        self.port = port
        self.tcp_port = tcp_port
        self.pidfile = pidfile
        self.logs_path = logs_path
        self.works_path = works_path
        self.cluster_name = cluster_name
        self.network_publish_host = network_publish_host
        self.index_store_type = index_store_type
        super().__init__(
            self._exec_command(),
            'http://{host}:{port}'.format(
                host=self.host,
                port=self.port,
            ),
            timeout=timeout
        )

    @property
    def version(self):
        """
        Get the given elasticsearch executable version parts.

        :return: Elasticsearch version
        :rtype: pkg_resources.Version
        """
        if not self._version:
            try:
                output = check_output([self.executable, '-Vv']).decode('utf-8')
                match = re.search(
                    r'Version: (?P<major>\d)\.(?P<minor>\d)\.(?P<patch>\d+)',
                    output
                )
                if not match:
                    raise RuntimeError(
                        "Elasticsearch version is not recognized. "
                        "It is probably not supported. \n"
                        "Output is: " + output)
                version = match.groupdict()
                self._version = parse_version(
                    '.'.join([
                        version['major'], version['minor'], version['patch']
                    ])
                )
            except OSError:
                raise RuntimeError(
                    "'%s' does not point to elasticsearch." % self.executable
                )
        return self._version

    def _exec_command(self):
        """
        Get command to run elasticsearch binary based on the version.

        :return: command to run elasticsearch
        :rtype: str
        """
        if self.version < parse_version('5.0.0'):
            raise RuntimeError("This elasticsearch version is not supported.")
        return '''
            {deamon} -p {pidfile}
            -E http.port={port}
            -E transport.tcp.port={tcp_port}
            -E path.logs={logs_path}
            -E path.data={work_path}
            -E cluster.name={cluster}
            -E network.host='{network_publish_host}'
            -E index.store.type={index_store_type}
        '''.format(
            deamon=self.executable,
            pidfile=self.pidfile,
            port=self.port,
            tcp_port=self.tcp_port,
            logs_path=self.logs_path,
            work_path=self.works_path,
            cluster=self.cluster_name,
            network_publish_host=self.network_publish_host,
            index_store_type=self.index_store_type,
        )
