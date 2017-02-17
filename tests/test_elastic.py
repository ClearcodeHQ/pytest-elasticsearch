"""Pytest-elasticsearch tests."""
from tempfile import gettempdir

from mock import patch

from pytest_elasticsearch import factories


def test_elastic_process(elasticsearch_proc):
    """Simple test for starting elasticsearch_proc."""
    assert elasticsearch_proc.running() is True


def test_elasticsearch(elasticsearch):
    """Test if elasticsearch fixtures connects to process."""
    info = elasticsearch.info()
    assert info['tagline'] == 'You Know, for Search'


elasticsearch_proc_random = factories.elasticsearch_proc(port=None)
elasticsearch_random = factories.elasticsearch('elasticsearch_proc_random')


def test_random_port(elasticsearch_random):
    """Test if elasticsearch fixture can be started on random port."""
    assert elasticsearch_random.info()['tagline'] == 'You Know, for Search'


def test_default_configuration(request):
    """Test default configuration."""
    config = factories.return_config(request)

    assert config['logsdir'] == gettempdir()
    assert not config['port']
    assert config['host'] == '127.0.0.1'
    assert not config['cluster_name']
    assert config['network_publish_host'] == '127.0.0.1'
    assert config['discovery_zen_ping_multicast_enabled'] == 'false'
    assert config['index_store_type'] == ''
    assert config['logs_prefix'] == ''

    logsdir_ini = request.config.getini('elasticsearch_logsdir')
    logsdir_option = request.config.getoption('elasticsearch_logsdir')

    assert logsdir_ini == gettempdir()
    assert logsdir_option is None


def test_version_specific_index_store_default(elasticsearch_proc):
    """Test version-specific default configuration of index.store.type."""
    command = elasticsearch_proc.command_parts

    assert 'index.store.type=fs' in command or 'index.store.type=memory' in command


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
    path_logs = 'default.path.logs=/tmp/elasticsearch_{}_logs'.format(port)

    assert conf_dict['logsdir'] == '/test1'
    assert path_logs in command
