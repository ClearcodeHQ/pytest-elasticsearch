"""Configuration for pytest-elasticsearch."""
from pathlib import Path
from typing import Any, Optional, TypedDict

from pytest import FixtureRequest


class ElasticsearchConfigDict(TypedDict):
    """Typed Config dictionary."""

    executable: Path
    host: str
    port: Optional[int]
    transport_tcp_port: Optional[int]
    cluster_name: str
    network_publish_host: str
    index_store_type: str


def get_config(request: FixtureRequest) -> ElasticsearchConfigDict:
    """Return a dictionary with config options."""

    def get_elasticsearch_option(option: str) -> Any:
        name = "elasticsearch_" + option
        return request.config.getoption(name) or request.config.getini(name)

    return ElasticsearchConfigDict(
        executable=get_elasticsearch_option("executable"),
        host=get_elasticsearch_option("host"),
        port=get_elasticsearch_option("port"),
        transport_tcp_port=get_elasticsearch_option("transport_tcp_port"),
        cluster_name=get_elasticsearch_option("cluster_name"),
        network_publish_host=get_elasticsearch_option("network_publish_host"),
        index_store_type=get_elasticsearch_option("index_store_type"),
    )
