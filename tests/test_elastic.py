"""Pytest-elasticsearch tests."""

from datetime import datetime
from pathlib import Path

import mock
import pytest
from elasticsearch import Elasticsearch
from packaging.version import Version
from pytest import FixtureRequest

import pytest_elasticsearch.config
from pytest_elasticsearch.executor import ElasticSearchExecutor

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

VERSION_STRING_7_17 = (
    "OpenJDK 64-Bit Server VM warning: Option UseConcMarkSweepGC was "
    "deprecated in version 9.0 and will likely be removed in a future release."
    "\nVersion: 7.17.0, Build: default/tar/bee86328705acaa9a6daede7140defd4d9ec56bd/"
    "2022-01-28T08:36:04.875279988Z, JVM: 11.0.14"
)

VERSION_STRING_8_0 = (
    "Version: 8.0.0, Build: default/tar/1b6a7ece17463df5ff54a3e1302d825889aa1161/"
    "2022-02-03T16:47:57.507843096Z, JVM: 17.0.1"
)


@pytest.mark.parametrize(
    "output, expected_version",
    (
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
        (VERSION_STRING_7_17, "7.17.0"),
        (VERSION_STRING_8_0, "8.0.0"),
    ),
)
def test_version_extraction(output: str, expected_version: str) -> None:
    """Verify if we can properly extract elasticsearch version."""
    with mock.patch(
        "pytest_elasticsearch.executor.check_output", lambda *args: output.encode("utf8")
    ):
        executor = ElasticSearchExecutor(
            executable=Path("elasticsearch"),
            host="127.0.0.1",
            port=8888,
            tcp_port=8889,
            pidfile=Path("elasticsearch.pid"),
            logs_path=Path("logs"),
            works_path=Path("works"),
            cluster_name="dontstart",
            network_publish_host="localhost",
            index_store_type="memory",
            timeout=10,
        )
        assert executor.version == Version(expected_version)


def test_elastic_process(elasticsearch_proc: ElasticSearchExecutor) -> None:
    """Simple test for starting elasticsearch_proc."""
    assert elasticsearch_proc.running() is True


def test_elasticsearch(elasticsearch: Elasticsearch) -> None:
    """Test if elasticsearch fixtures connects to process."""
    info = elasticsearch.cluster.health()
    assert info["status"] == "green"


def test_default_configuration(request: FixtureRequest) -> None:
    """Test default configuration."""
    config = pytest_elasticsearch.config.get_config(request)

    assert not config["port"]
    assert config["host"] == "127.0.0.1"
    assert not config["cluster_name"]
    assert config["network_publish_host"] == "127.0.0.1"
    assert config["index_store_type"] == "mmapfs"


def test_external_elastic(
    elasticsearch2: Elasticsearch,
    elasticsearch2_noop: Elasticsearch,
) -> None:
    """Check that nooproc connects to the same redis."""
    elasticsearch2.indices.create(index="test-index")
    doc = {
        "author": "kimchy",
        "text": "Elasticsearch: cool. bonsai cool.",
        "timestamp": datetime.utcnow(),
    }
    res = elasticsearch2.index(index="test-index", id="1", document=doc)
    assert res["result"] == "created"

    res = elasticsearch2_noop.get(index="test-index", id="1")
    assert res["found"] is True
    elasticsearch2.indices.refresh(index="test-index")

    res = elasticsearch2_noop.search(index="test-index", query={"match_all": {}})
    assert res["hits"]["total"]["value"] == 1
