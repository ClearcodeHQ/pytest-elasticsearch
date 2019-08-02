"""Pytest-elasticsearch tests."""
from tempfile import gettempdir
import pytest

from pytest_elasticsearch import factories

ELASTICSEARCH_EXECUTABLE_5_6 = '/opt/es/elasticsearch-5.6.16/bin/elasticsearch'
ELASTICSEARCH_EXECUTABLE_6_8 = '/opt/es/elasticsearch-6.8.2/bin/elasticsearch'
ELASTICSEARCH_EXECUTABLE_7_3 = '/opt/es/elasticsearch-7.3.0/bin/elasticsearch'


def elasticsearch_fixture_factory(executable, proc_name, port, **kwargs):
    """Create elasticsearch fixture pairs."""
    proc = factories.elasticsearch_proc(executable, port=port, **kwargs)
    elasticsearch = factories.elasticsearch(proc_name)
    return proc, elasticsearch


# pylint:disable=invalid-name
elasticsearch_proc_5_6, elasticsearch_5_6 = elasticsearch_fixture_factory(
    ELASTICSEARCH_EXECUTABLE_5_6, 'elasticsearch_proc_5_6', port=None
)
elasticsearch_proc_6_8, elasticsearch_6_8 = elasticsearch_fixture_factory(
    ELASTICSEARCH_EXECUTABLE_6_8, 'elasticsearch_proc_6_8', port=None
)
elasticsearch_proc_7_3, elasticsearch_7_3 = elasticsearch_fixture_factory(
    ELASTICSEARCH_EXECUTABLE_7_3, 'elasticsearch_proc_7_3', port=None
)
# pylint:enable=invalid-name


@pytest.mark.parametrize('executable, expected_version', (
    (ELASTICSEARCH_EXECUTABLE_5_6, '5.6.16'),
    (ELASTICSEARCH_EXECUTABLE_6_8, '6.8.2'),
    (ELASTICSEARCH_EXECUTABLE_7_3, '7.3.0'),
))
def test_version_extraction(executable, expected_version):
    """Verfiy if we can properly extract elasticsearch version."""
    ver = factories.get_version_parts(executable)
    assert ver.base_version == expected_version


@pytest.mark.parametrize('elasticsearch_proc_name', (
    'elasticsearch_proc_5_6',
    'elasticsearch_proc_6_8',
    'elasticsearch_proc_7_3',
))
def test_elastic_process(request, elasticsearch_proc_name):
    """Simple test for starting elasticsearch_proc."""
    elasticsearch_proc = request.getfixturevalue(elasticsearch_proc_name)
    assert elasticsearch_proc.running() is True


@pytest.mark.parametrize('elasticsearch_name', (
    'elasticsearch_5_6',
    'elasticsearch_6_8',
    'elasticsearch_7_3',
))
def test_elasticsarch(request, elasticsearch_name):
    """Test if elasticsearch fixtures connects to process."""
    elasticsearch = request.getfixturevalue(elasticsearch_name)
    info = elasticsearch.cluster.health()
    assert info['status'] == 'green'


def test_default_configuration(request):
    """Test default configuration."""
    config = factories.return_config(request)

    assert config['logsdir'] == gettempdir()
    assert not config['port']
    assert config['host'] == '127.0.0.1'
    assert not config['cluster_name']
    assert config['network_publish_host'] == '127.0.0.1'
    assert config['discovery_zen_ping_multicast_enabled'] == 'false'
    assert config['index_store_type'] == 'memory'
    assert config['logs_prefix'] == ''

    logsdir_ini = request.config.getini('elasticsearch_logsdir')
    logsdir_option = request.config.getoption('elasticsearch_logsdir')

    assert logsdir_ini == '/tmp'
    assert logsdir_option is None
