"""Pytest-elasticsearch tests."""
from datetime import datetime
from tempfile import gettempdir

import mock
import pytest
from pkg_resources import parse_version

from pytest_elasticsearch import factories
from pytest_elasticsearch.executor import ElasticSearchExecutor


VERSION_STRING_5_6 = (
    'OpenJDK 64-Bit Server VM warning: Option UseConcMarkSweepGC was '
    'deprecated in version 9.0 and will likely be removed in a future release.'
    '\nVersion: 5.6.16, Build: 3a740d1/2019-03-13T15:33:36.565Z, JVM: 11.0.2'
)
VERSION_STRING_6_8 = (
    'OpenJDK 64-Bit Server VM warning: Option UseConcMarkSweepGC was '
    'deprecated in version 9.0 and will likely be removed in a future release.'
    '\nVersion: 6.8.12, Build: default/zip/7a15d2a/2020-08-12T07:27:20.804867Z,'
    ' JVM: 11.0.2'
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
    '\nVersion: 7.4.2, Build: default/tar/2f90bbf7b93631e52bafb59b3b049cb44ec25'
    'e96/2019-10-28T20:40:44.881551Z, JVM: 11.0.2'
)
VERSION_STRING_7_5 = (
    'OpenJDK 64-Bit Server VM warning: Option UseConcMarkSweepGC was '
    'deprecated in version 9.0 and will likely be removed in a future release.'
    '\nVersion: 7.5.2, Build: default/tar/8bec50e1e0ad29dad5653712cf3bb580cd1af'
    'cdf/2020-01-15T12:11:52.313576Z, JVM: 11.0.2'
)
VERSION_STRING_7_6 = (
    'OpenJDK 64-Bit Server VM warning: Option UseConcMarkSweepGC was '
    'deprecated in version 9.0 and will likely be removed in a future release.'
    '\nVersion: 7.6.2, Build: default/tar/ef48eb35cf30adf4db14086e8aabd07ef6fb1'
    '13f/2020-03-26T06:34:37.794943Z, JVM: 11.0.2'
)
VERSION_STRING_7_7 = (
    'OpenJDK 64-Bit Server VM warning: Option UseConcMarkSweepGC was '
    'deprecated in version 9.0 and will likely be removed in a future release.'
    '\nVersion: 7.7.1, Build: default/tar/ad56dce891c901a492bb1ee393f12dfff473a'
    '423/2020-05-28T16:30:01.040088Z, JVM: 11.0.2'
)
VERSION_STRING_7_8 = (
    'OpenJDK 64-Bit Server VM warning: Option UseConcMarkSweepGC was '
    'deprecated in version 9.0 and will likely be removed in a future release.'
    '\nVersion: 7.8.1, Build: default/tar/b5ca9c58fb664ca8bf9e4057fc229b3396bf3'
    'a89/2020-07-21T16:40:44.668009Z, JVM: 11.0.2'
)
VERSION_STRING_7_9 = (
    'OpenJDK 64-Bit Server VM warning: Option UseConcMarkSweepGC was '
    'deprecated in version 9.0 and will likely be removed in a future release.'
    '\nVersion: 7.9.0, Build: default/tar/a479a2a7fce0389512d6a9361301708b92dff'
    '667/2020-08-11T21:36:48.204330Z, JVM: 11.0.2'
)


@pytest.mark.parametrize('output, expected_version', (
    (VERSION_STRING_5_6, '5.6.16'),
    (VERSION_STRING_6_8, '6.8.12'),
    (VERSION_STRING_7_3, '7.3.0'),
    (VERSION_STRING_7_3_2, '7.3.2'),
    (VERSION_STRING_7_4, '7.4.2'),
    (VERSION_STRING_7_5, '7.5.2'),
    (VERSION_STRING_7_6, '7.6.2'),
    (VERSION_STRING_7_7, '7.7.1'),
    (VERSION_STRING_7_8, '7.8.1'),
    (VERSION_STRING_7_9, '7.9.0'),
))
def test_version_extraction(output, expected_version):
    """Verify if we can properly extract elasticsearch version."""
    with mock.patch(
            'pytest_elasticsearch.executor.check_output',
            lambda *args, **kwargs: output.encode('utf8')
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
    'elasticsearch_proc_7_4',
    'elasticsearch_proc_7_5',
    'elasticsearch_proc_7_6',
    'elasticsearch_proc_7_7',
    'elasticsearch_proc_7_8',
    'elasticsearch_proc_7_9',
))
def test_elastic_process(request, elasticsearch_proc_name):
    """Simple test for starting elasticsearch_proc."""
    elasticsearch_proc = request.getfixturevalue(elasticsearch_proc_name)
    assert elasticsearch_proc.running() is True


@pytest.mark.parametrize('elasticsearch_name', (
    'elasticsearch_5_6',
    'elasticsearch_6_8',
    'elasticsearch_7_4',
    'elasticsearch_7_5',
    'elasticsearch_7_6',
    'elasticsearch_7_7',
    'elasticsearch_7_8',
    'elasticsearch_7_9',
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
    assert config['index_store_type'] == 'mmapfs'
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
    res = elasticsearch2.index(
        index="test-index", doc_type='tweet', id=1, body=doc
    )
    assert res['result'] == 'created'

    res = elasticsearch2_noop.get(index="test-index", doc_type='tweet', id=1)
    assert res['found'] is True
    elasticsearch2.indices.refresh(index="test-index")

    res = elasticsearch2_noop.search(
        index="test-index", body={"query": {"match_all": {}}}
    )
    assert res['hits']['total']['value'] == 1
