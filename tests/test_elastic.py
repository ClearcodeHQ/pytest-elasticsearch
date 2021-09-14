"""Pytest-elasticsearch tests."""
from datetime import datetime
from tempfile import gettempdir

import mock
import pytest
from pkg_resources import parse_version

from pytest_elasticsearch import factories
from pytest_elasticsearch.executor import ElasticSearchExecutor


VERSION_STRING_6_8 = (
    "OpenJDK 64-Bit Server VM warning: Option UseConcMarkSweepGC was "
    "deprecated in version 9.0 and will likely be removed in a future release."
    "\nVersion: 6.8.12, Build: default/zip/7a15d2a/2020-08-12T07:27:20.804867Z,"
    " JVM: 11.0.2"
)
VERSION_STRING_7_3 = (
    "OpenJDK 64-Bit Server VM warning: Option UseConcMarkSweepGC was "
    "deprecated in version 9.0 and will likely be removed in a future release."
    "\nVersion: 7.3.0, Build: default/tar/de777fa/2019-07-24T18:30:11.767338Z, "
    "JVM: 11.0.2"
)
VERSION_STRING_7_3_2 = (
    "OpenJDK 64-Bit Server VM warning: Option UseConcMarkSweepGC was "
    "deprecated in version 9.0 and will likely be removed in a future release."
    "\nVersion: 7.3.2, Build: default/tar/1c1faf1/2019-09-06T14:40:30.409026Z, "
    "JVM: 11.0.2"
)
VERSION_STRING_7_4 = (
    "OpenJDK 64-Bit Server VM warning: Option UseConcMarkSweepGC was "
    "deprecated in version 9.0 and will likely be removed in a future release."
    "\nVersion: 7.4.2, Build: default/tar/2f90bbf7b93631e52bafb59b3b049cb44ec25"
    "e96/2019-10-28T20:40:44.881551Z, JVM: 11.0.2"
)
VERSION_STRING_7_5 = (
    "OpenJDK 64-Bit Server VM warning: Option UseConcMarkSweepGC was "
    "deprecated in version 9.0 and will likely be removed in a future release."
    "\nVersion: 7.5.2, Build: default/tar/8bec50e1e0ad29dad5653712cf3bb580cd1af"
    "cdf/2020-01-15T12:11:52.313576Z, JVM: 11.0.2"
)
VERSION_STRING_7_6 = (
    "OpenJDK 64-Bit Server VM warning: Option UseConcMarkSweepGC was "
    "deprecated in version 9.0 and will likely be removed in a future release."
    "\nVersion: 7.6.2, Build: default/tar/ef48eb35cf30adf4db14086e8aabd07ef6fb1"
    "13f/2020-03-26T06:34:37.794943Z, JVM: 11.0.2"
)
VERSION_STRING_7_7 = (
    "OpenJDK 64-Bit Server VM warning: Option UseConcMarkSweepGC was "
    "deprecated in version 9.0 and will likely be removed in a future release."
    "\nVersion: 7.7.1, Build: default/tar/ad56dce891c901a492bb1ee393f12dfff473a"
    "423/2020-05-28T16:30:01.040088Z, JVM: 11.0.2"
)
VERSION_STRING_7_8 = (
    "OpenJDK 64-Bit Server VM warning: Option UseConcMarkSweepGC was "
    "deprecated in version 9.0 and will likely be removed in a future release."
    "\nVersion: 7.8.1, Build: default/tar/b5ca9c58fb664ca8bf9e4057fc229b3396bf3"
    "a89/2020-07-21T16:40:44.668009Z, JVM: 11.0.2"
)
VERSION_STRING_7_9 = (
    "OpenJDK 64-Bit Server VM warning: Option UseConcMarkSweepGC was "
    "deprecated in version 9.0 and will likely be removed in a future release."
    "\nVersion: 7.9.0, Build: default/tar/a479a2a7fce0389512d6a9361301708b92dff"
    "667/2020-08-11T21:36:48.204330Z, JVM: 11.0.2"
)

VERSION_STRING_7_10 = (
    "OpenJDK 64-Bit Server VM warning: Option UseConcMarkSweepGC was "
    "deprecated in version 9.0 and will likely be removed in a future release."
    "\nVersion: 7.10.0, "
    "Build: default/tar/a479a2a7fce0389512d6a9361301708b92dff667/"
    "2020-08-11T21:36:48.204330Z, JVM: 11.0.2"
)

VERSION_STRING_7_12 = (
    "Version: 7.12.1, Build: default/deb/3186837139b9c6b6d23c3200870651f10d3343b7/"
    "2021-04-20T20:56:39.040728659Z, JVM: 16"
)

VERSION_STRING_7_14 = (
    "OpenJDK 64-Bit Server VM warning: Option UseConcMarkSweepGC was "
    "deprecated in version 9.0 and will likely be removed in a future release."
    "\nVersion: 7.14.1, Build: default/tar/66b55ebfa59c92c15db3f69a335d500018b3331e/"
    "2021-08-26T09:01:05.390870785Z, JVM: 11.0.11"
)


@pytest.mark.parametrize(
    "output, expected_version",
    (
        (VERSION_STRING_6_8, "6.8.12"),
        (VERSION_STRING_7_3, "7.3.0"),
        (VERSION_STRING_7_3_2, "7.3.2"),
        (VERSION_STRING_7_4, "7.4.2"),
        (VERSION_STRING_7_5, "7.5.2"),
        (VERSION_STRING_7_6, "7.6.2"),
        (VERSION_STRING_7_7, "7.7.1"),
        (VERSION_STRING_7_8, "7.8.1"),
        (VERSION_STRING_7_9, "7.9.0"),
        (VERSION_STRING_7_10, "7.10.0"),
        (VERSION_STRING_7_12, "7.12.1"),
        (VERSION_STRING_7_14, "7.14.1"),
    ),
)
def test_version_extraction(output, expected_version):
    """Verify if we can properly extract elasticsearch version."""
    with mock.patch(
        "pytest_elasticsearch.executor.check_output", lambda *args: output.encode("utf8")
    ):
        executor = ElasticSearchExecutor(
            "elasticsearch", "127.0.0.1", 8888, None, None, None, None, None, None, None, 10
        )
        assert executor.version == parse_version(expected_version)


def test_elastic_process(elasticsearch_proc):
    """Simple test for starting elasticsearch_proc."""
    assert elasticsearch_proc.running() is True


def test_elasticsearch(elasticsearch):
    """Test if elasticsearch fixtures connects to process."""
    info = elasticsearch.cluster.health()
    assert info["status"] == "green"


def test_default_configuration(request):
    """Test default configuration."""
    config = factories.return_config(request)

    assert config["logsdir"] == gettempdir()
    assert not config["port"]
    assert config["host"] == "127.0.0.1"
    assert not config["cluster_name"]
    assert config["network_publish_host"] == "127.0.0.1"
    assert config["index_store_type"] == "mmapfs"
    assert config["logs_prefix"] == ""

    logsdir_ini = request.config.getini("elasticsearch_logsdir")
    logsdir_option = request.config.getoption("elasticsearch_logsdir")

    assert logsdir_ini == "/tmp"
    assert logsdir_option is None


def test_external_elastic(elasticsearch2, elasticsearch_proc2, elasticsearch2_noop):
    """Check that nooproc connects to the same redis."""
    if elasticsearch_proc2.version < parse_version("7.0.0"):
        pytest.skip("Search response differes for earlier versions")
    elasticsearch2.indices.create(index="test-index", ignore=400)
    doc = {
        "author": "kimchy",
        "text": "Elasticsearch: cool. bonsai cool.",
        "timestamp": datetime.utcnow(),
    }
    res = elasticsearch2.index(index="test-index", doc_type="tweet", id=1, body=doc)
    assert res["result"] == "created"

    res = elasticsearch2_noop.get(index="test-index", doc_type="tweet", id=1)
    assert res["found"] is True
    elasticsearch2.indices.refresh(index="test-index")

    res = elasticsearch2_noop.search(index="test-index", body={"query": {"match_all": {}}})
    assert res["hits"]["total"]["value"] == 1
