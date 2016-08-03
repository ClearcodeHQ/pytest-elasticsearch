"""Pytest-elasticsearch tests."""
from mock import patch

from pytest_elasticsearch import factories


def test_elastic_process(elasticsearch_proc):
    """Simple test for starting elasticsearch_proc."""
    assert elasticsearch_proc.running() is True


def test_elasticsarch(elasticsearch):
    """Test if elasticsearch fixtures connects to process."""
    assert elasticsearch.cluster.health()['status'] == 'green'


elasticsearch_proc_random = factories.elasticsearch_proc(port=None)
elasticsearch_random = factories.elasticsearch('elasticsearch_proc_random')


def test_random_port(elasticsearch_random):
    """Test if elasticsearch fixture can be started on random port."""
    assert elasticsearch_random.cluster.health()['status'] == 'green'


def test_index_creation(elasticsearch):
    """Test if index creation via elasticsearch fixture succeeds."""
    name = 'mytestindex'
    elasticsearch.indices.create(index=name)
    assert name in elasticsearch.indices.get_settings().keys()


def test_default_configuration(request):
    """
    Test default configuration.

    (Works only if not command line option is passed.)
    """
    default_config = {
        'logsdir': '/tmp', 'discovery_zen_ping_multicast_enabled': 'false',
        'index_store_type': '', 'network_publish_host': '127.0.0.1',
        'cluster_name': 'elasticsearch_cluster_9201', 'host': '127.0.0.1',
        'logs_prefix': '', 'port': 9201
    }

    options = (
        'logsdir', 'port', 'host', 'cluster_name',
        'network_publish_host', 'discovery_zen_ping_multicast_enabled',
        'index_store_type', 'logs_prefix'
    )

    config = factories.return_config(request)

    for option in options:
        if not request.config.getoption(option):
            assert config[option] == default_config[option]


@patch('pytest_elasticsearch.plugin.pytest.config')
def test_ini_option_configuration(request):
    """Test if ini and option configuration works in proper way."""
    request.config.getoption.return_value = None
    request.config.getini.return_value = '/test1'

    assert '/test1' == factories.return_config(request)['logsdir']

    request.config.getoption.return_value = '/test2'
    request.config.getini.return_value = None

    assert '/test2' == factories.return_config(request)['logsdir']

elasticsearch_proc_args = factories.elasticsearch_proc(
    port=None, elasticsearch_logsdir='/tmp')


@patch('pytest_elasticsearch.plugin.pytest.config')
def test_fixture_arg_is_first(request, elasticsearch_proc_args):
    """Test if arg comes first than opt and ini."""
    request.config.getoption.return_value = '/test1'
    request.config.getini.return_value = '/test2'
    conf_dict = factories.return_config(request)

    port = elasticsearch_proc_args.port
    command = elasticsearch_proc_args.command_parts
    path_logs = '--default.path.logs=/tmp/elasticsearch_{}_logs'.format(port)

    assert conf_dict['logsdir'] == '/test1'
    assert path_logs in command
