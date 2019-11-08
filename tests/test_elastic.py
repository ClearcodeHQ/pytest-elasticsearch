"""Pytest-elasticsearch tests."""
from datetime import datetime
from tempfile import gettempdir

import mock
import pytest
from pkg_resources import parse_version

from pytest_elasticsearch import factories
from pytest_elasticsearch.executor import ElasticSearchExecutor

ELASTICSEARCH_EXECUTABLE_5_6 = '/opt/es/elasticsearch-5.6.16/bin/elasticsearch'
ELASTICSEARCH_EXECUTABLE_6_8 = '/opt/es/elasticsearch-6.8.3/bin/elasticsearch'
ELASTICSEARCH_EXECUTABLE_7_3 = '/opt/es/elasticsearch-7.3.2/bin/elasticsearch'
ELASTICSEARCH_EXECUTABLE_7_4 = '/opt/es/elasticsearch-7.4.1/bin/elasticsearch'

VERSION_STRING_5_6 = (
    'OpenJDK 64-Bit Server VM warning: Option UseConcMarkSweepGC was '
    'deprecated in version 9.0 and will likely be removed in a future release.'
    '\nVersion: 5.6.16, Build: 3a740d1/2019-03-13T15:33:36.565Z, JVM: 11.0.2'
)
VERSION_STRING_6_8 = (
    'OpenJDK 64-Bit Server VM warning: Option UseConcMarkSweepGC was '
    'deprecated in version 9.0 and will likely be removed in a future release.'
    '\nVersion: 6.8.2, Build: default/zip/b506955/2019-07-24T15:24:41.545295Z, '
    'JVM: 11.0.2'
)
VERSION_STRING_6_8_3 = (
    'OpenJDK 64-Bit Server VM warning: Option UseConcMarkSweepGC was '
    'deprecated in version 9.0 and will likely be removed in a future release.'
    '\nVersion: 6.8.3, Build: default/zip/0c48c0e/2019-08-29T19:05:24.312154Z, '
    'JVM: 11.0.2'
)
VERSION_STRING_7_3 = (
    'OpenJDK 64-Bit Server VM warning: Option UseConcMarkSweepGC was '
    'deprecated in version 9.0 and will likely be removed in a future release.'
    '\nVersion: 7.3.0, Build: default/tar/de777fa/2019-07-24T18:30:11.767338Z, '
    'JVM: 11.0.2'
)
VERSION_STRING_7_3_2 = (
    'OpenJDK 64-Bit Server VM warning: Option UseConcMarkSweepGC was '
    'deprecated in version 9.0 and will likely be removed in a future release.'
    '\nVersion: 7.3.2, Build: default/tar/1c1faf1/2019-09-06T14:40:30.409026Z, '
    'JVM: 11.0.2'
)
VERSION_STRING_7_4 = (
    'OpenJDK 64-Bit Server VM warning: Option UseConcMarkSweepGC was '
    'deprecated in version 9.0 and will likely be removed in a future release.'
    '\nVersion: 7.4.1, Build: default/tar/fc0eeb6e2c25915d63d871d344e3d0b45ea0e'
    'a1e/2019-10-22T17:16:35.176724Z, JVM: 11.0.2'
)


def elasticsearch_fixture_factory(executable, proc_name, port, **kwargs):
    """Create elasticsearch fixture pairs."""
    proc = factories.elasticsearch_proc(executable, port=port, **kwargs)
    elasticsearch = factories.elasticsearch(proc_name)
    return proc, elasticsearch


# pylint:disable=invalid-name
elasticsearch_proc2 = factories.elasticsearch_proc(executable=ELASTICSEARCH_EXECUTABLE_7_4, port=9393)
elasticsearch_nooproc2 = factories.elasticsearch_noproc(port=9393)
elasticsearch2 = factories.elasticsearch('elasticsearch_proc2')
elasticsearch2_noop = factories.elasticsearch('elasticsearch_nooproc2')
# pylint:enable=invalid-name


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
elasticsearch_proc_7_4, elasticsearch_7_4 = elasticsearch_fixture_factory(
    ELASTICSEARCH_EXECUTABLE_7_4, 'elasticsearch_proc_7_4', port=None
)
# pylint:enable=invalid-name


@pytest.mark.parametrize('output, expected_version', (
    (VERSION_STRING_5_6, '5.6.16'),
    (VERSION_STRING_6_8, '6.8.2'),
    (VERSION_STRING_6_8_3, '6.8.3'),
    (VERSION_STRING_7_3, '7.3.0'),
    (VERSION_STRING_7_3_2, '7.3.2'),
    (VERSION_STRING_7_4, '7.4.1'),
))
def test_version_extraction(output, expected_version):
    """Verify if we can properly extract elasticsearch version."""
    with mock.patch(
            'pytest_elasticsearch.executor.check_output',
            lambda *args: output.encode('utf8')
    ):
        executor = ElasticSearchExecutor(
            'elasticsearch',
            '127.0.0.1', 8888,
            None, None, None, None, None, None, None,
            10
        )
        assert executor.version == parse_version(expected_version)


@pytest.mark.parametrize('elasticsearch_proc_name', (
    'elasticsearch_proc_5_6',
    'elasticsearch_proc_6_8',
    'elasticsearch_proc_7_3',
    'elasticsearch_proc_7_4',
))
def test_elastic_process(request, elasticsearch_proc_name):
    """Simple test for starting elasticsearch_proc."""
    elasticsearch_proc = request.getfixturevalue(elasticsearch_proc_name)
    assert elasticsearch_proc.running() is True


@pytest.mark.parametrize('elasticsearch_name', (
    'elasticsearch_5_6',
    'elasticsearch_6_8',
    'elasticsearch_7_3',
    'elasticsearch_7_4',
))
def test_elasticsearch(request, elasticsearch_name):
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
    assert config['index_store_type'] == 'memory'
    assert config['logs_prefix'] == ''

    logsdir_ini = request.config.getini('elasticsearch_logsdir')
    logsdir_option = request.config.getoption('elasticsearch_logsdir')

    assert logsdir_ini == '/tmp'
    assert logsdir_option is None


def test_external_elastic(elasticsearch2, elasticsearch2_noop):
    """Check that nooproc connects to the same redis."""
    elasticsearch2.indices.create(index='test-index', ignore=400)
    doc = {
        'author': 'kimchy',
        'text': 'Elasticsearch: cool. bonsai cool.',
        'timestamp': datetime.utcnow(),
    }
    import pdb; pdb.set_trace()
    res = elasticsearch2.index(index="test-index", doc_type='tweet', id=1, body=doc)
    assert res['result'] == 'created'

    res = elasticsearch2_noop.get(index="test-index", doc_type='tweet', id=1)
    assert res['found'] == True
    elasticsearch2.indices.refresh(index="test-index")

    res = elasticsearch2_noop.search(index="test-index", body={"query": {"match_all": {}}})
    assert res['hits']['total']['value'] == 1
