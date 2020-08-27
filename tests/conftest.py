"""Tests main conftest file."""
import warnings

from pytest_elasticsearch import factories

warnings.simplefilter("error", category=DeprecationWarning)


ELASTICSEARCH_EXECUTABLE_5_6 = '/opt/es/elasticsearch-5.6.16/bin/elasticsearch'
ELASTICSEARCH_EXECUTABLE_6_8 = '/opt/es/elasticsearch-6.8.12/bin/elasticsearch'
ELASTICSEARCH_EXECUTABLE_7_4 = '/opt/es/elasticsearch-7.4.2/bin/elasticsearch'
ELASTICSEARCH_EXECUTABLE_7_5 = '/opt/es/elasticsearch-7.5.2/bin/elasticsearch'
ELASTICSEARCH_EXECUTABLE_7_6 = '/opt/es/elasticsearch-7.6.2/bin/elasticsearch'
ELASTICSEARCH_EXECUTABLE_7_7 = '/opt/es/elasticsearch-7.7.1/bin/elasticsearch'
ELASTICSEARCH_EXECUTABLE_7_8 = '/opt/es/elasticsearch-7.8.1/bin/elasticsearch'
ELASTICSEARCH_EXECUTABLE_7_9 = '/opt/es/elasticsearch-7.9.0/bin/elasticsearch'


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
elasticsearch_proc_7_4, elasticsearch_7_4 = elasticsearch_fixture_factory(
    ELASTICSEARCH_EXECUTABLE_7_4, 'elasticsearch_proc_7_4', port=None
)
elasticsearch_proc_7_5, elasticsearch_7_5 = elasticsearch_fixture_factory(
    ELASTICSEARCH_EXECUTABLE_7_5, 'elasticsearch_proc_7_5', port=None
)
elasticsearch_proc_7_6, elasticsearch_7_6 = elasticsearch_fixture_factory(
    ELASTICSEARCH_EXECUTABLE_7_6, 'elasticsearch_proc_7_6', port=None
)
elasticsearch_proc_7_7, elasticsearch_7_7 = elasticsearch_fixture_factory(
    ELASTICSEARCH_EXECUTABLE_7_7, 'elasticsearch_proc_7_7', port=None
)
elasticsearch_proc_7_8, elasticsearch_7_8 = elasticsearch_fixture_factory(
    ELASTICSEARCH_EXECUTABLE_7_8, 'elasticsearch_proc_7_8', port=None
)
elasticsearch_proc_7_9, elasticsearch_7_9 = elasticsearch_fixture_factory(
    ELASTICSEARCH_EXECUTABLE_7_9, 'elasticsearch_proc_7_9', port=None
)

elasticsearch_proc2 = factories.elasticsearch_proc(
    executable=ELASTICSEARCH_EXECUTABLE_7_9, port=9393
)
elasticsearch_nooproc2 = factories.elasticsearch_noproc(port=9393)
elasticsearch2 = factories.elasticsearch('elasticsearch_proc2')
elasticsearch2_noop = factories.elasticsearch('elasticsearch_nooproc2')
# pylint:enable=invalid-name
