"""Pytest-elasticsearch tests."""
from tempfile import gettempdir
import pytest

from pytest_elasticsearch import factories

ELASTICSEARCH_CONF_PATH_1_5_2 = '/opt/elasticsearch-1.5.2/config'
ELASTICSEARCH_CONF_PATH_2_4_6 = '/opt/elasticsearch-2.4.6/config'
ELASTICSEARCH_EXECUTABLE_1_5_2 = '/opt/elasticsearch-1.5.2/bin/elasticsearch'
ELASTICSEARCH_EXECUTABLE_2_4_6 = '/opt/elasticsearch-2.4.6/bin/elasticsearch'
ELASTICSEARCH_EXECUTABLE_5_6_7 = '/opt/elasticsearch-5.6.7/bin/elasticsearch'
ELASTICSEARCH_EXECUTABLE_6_2_3 = '/opt/elasticsearch-6.2.3/bin/elasticsearch'


def elasticsearch_fixture_factory(executable, proc_name, port, **kwargs):
    """Create elasticsearch fixture pairs."""
    proc = factories.elasticsearch_proc(executable, port=port, **kwargs)
    elasticsearch = factories.elasticsearch(proc_name)
    return proc, elasticsearch


# pylint:disable=invalid-name
elasticsearch_proc_1_5_2, elasticsearch_1_5_2 = elasticsearch_fixture_factory(
    ELASTICSEARCH_EXECUTABLE_1_5_2, 'elasticsearch_proc_1_5_2',
    port=None, configuration_path=ELASTICSEARCH_CONF_PATH_1_5_2
)
elasticsearch_proc_2_4_6, elasticsearch_2_4_6 = elasticsearch_fixture_factory(
    ELASTICSEARCH_EXECUTABLE_2_4_6, 'elasticsearch_proc_2_4_6',
    port=None, configuration_path=ELASTICSEARCH_CONF_PATH_2_4_6
)
elasticsearch_proc_5_6_7, elasticsearch_5_6_7 = elasticsearch_fixture_factory(
    ELASTICSEARCH_EXECUTABLE_5_6_7, 'elasticsearch_proc_5_6_7', port=None
)
elasticsearch_proc_6_2_3, elasticsearch_6_2_3 = elasticsearch_fixture_factory(
    ELASTICSEARCH_EXECUTABLE_6_2_3, 'elasticsearch_proc_6_2_3', port=None
)

elasticsearch_proc_random = factories.elasticsearch_proc(
    ELASTICSEARCH_EXECUTABLE_1_5_2, port=None,
    configuration_path=ELASTICSEARCH_CONF_PATH_1_5_2
)
elasticsearch_random = factories.elasticsearch('elasticsearch_proc_random')
# pylint:enable=invalid-name


@pytest.mark.parametrize('elasticsearch_proc_name', (
    'elasticsearch_proc_1_5_2',
    'elasticsearch_proc_2_4_6',
    'elasticsearch_proc_5_6_7',
    'elasticsearch_proc_6_2_3'
))
def test_elastic_process(request, elasticsearch_proc_name):
    """Simple test for starting elasticsearch_proc."""
    elasticsearch_proc = request.getfixturevalue(elasticsearch_proc_name)
    assert elasticsearch_proc.running() is True


@pytest.mark.parametrize('elasticsearch_name', (
    'elasticsearch_1_5_2',
    'elasticsearch_2_4_6',
    'elasticsearch_5_6_7',
    'elasticsearch_6_2_3'
))
def test_elasticsarch(request, elasticsearch_name):
    """Test if elasticsearch fixtures connects to process."""
    elasticsearch = request.getfixturevalue(elasticsearch_name)
    info = elasticsearch.cluster.health()
    assert info['status'] == 'green'


@pytest.mark.parametrize('executable, expected_version', (
    (ELASTICSEARCH_EXECUTABLE_1_5_2, '1.5.2'),
    (ELASTICSEARCH_EXECUTABLE_2_4_6, '2.4.6'),
    (ELASTICSEARCH_EXECUTABLE_5_6_7, '5.6.7'),
    (ELASTICSEARCH_EXECUTABLE_6_2_3, '6.2.3')
))
def test_version_extraction(executable, expected_version):
    """Verfiy if we can properly extract elasticsearch version."""
    ver = factories.get_version_parts(executable)
    assert ver.base_version == expected_version


def test_random_port(  # pylint:disable=redefined-outer-name
        elasticsearch_random
):
    """Test if elasticsearch fixture can be started on random port."""
    assert elasticsearch_random.cluster.health()['status'] == 'green'


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
