"""Tests main conftest file."""
import warnings

from pytest_elasticsearch import factories

warnings.simplefilter("error", category=DeprecationWarning)



# pylint:disable=invalid-name
elasticsearch_proc2 = factories.elasticsearch_proc(port=6381)
elasticsearch_nooproc2 = factories.elasticsearch_noproc(port=6381)
elasticsearch2 = factories.elasticsearch('elasticsearch_proc2')
elasticsearch2_noop = factories.elasticsearch('elasticsearch_nooproc2')
# pylint:enable=invalid-name