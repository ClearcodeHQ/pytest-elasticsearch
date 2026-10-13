"""Run tests for executor."""

import json
from collections.abc import Iterator
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from threading import Thread
from unittest import mock

import pytest
from packaging.version import Version

from pytest_elasticsearch.executor import ElasticSearchExecutor

VERSION_STRING_8_0 = (
    "Version: 8.0.0, Build: default/tar/1b6a7ece17463df5ff54a3e1302d825889aa1161/"
    "2022-02-03T16:47:57.507843096Z, JVM: 17.0.1"
)
VERSION_STRING_8_15 = (
    "Version: 8.15.0, Build: default/tar/6f64a5184ddc8f708a2ddcc4ebf9d1d84b7f7e1b/"
    "2024-06-11T09:13:52.000000Z, JVM: 21.0.2"
)
VERSION_STRING_9_2 = (
    "Version: 9.2.0, Build: default/tar/1b6a7ece17463df5ff54a3e1302d825889aa1161/"
    "2025-03-11T09:13:52.000000Z, JVM: 21.0.2"
)


@pytest.mark.parametrize(
    "output, expected_version",
    (
        (VERSION_STRING_8_0, "8.0.0"),
        (VERSION_STRING_8_15, "8.15.0"),
        (VERSION_STRING_9_2, "9.2.0"),
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


def make_executor(port: int = 8888) -> ElasticSearchExecutor:
    """Build an executor without touching a real elasticsearch binary."""
    with mock.patch(
        "pytest_elasticsearch.executor.check_output",
        lambda *args: VERSION_STRING_9_2.encode("utf8"),
    ):
        return ElasticSearchExecutor(
            executable=Path("elasticsearch"),
            host="127.0.0.1",
            port=port,
            tcp_port=port + 1,
            pidfile=Path("elasticsearch.pid"),
            logs_path=Path("logs"),
            works_path=Path("works"),
            cluster_name="dontstart",
            network_publish_host="localhost",
            index_store_type="memory",
            timeout=10,
        )


class HealthHandler(BaseHTTPRequestHandler):
    """Answer every GET with the status code and body set on the server."""

    def do_GET(self) -> None:  # noqa: N802
        """Send the configured response."""
        code, body = self.server.response  # type: ignore[attr-defined]
        self.server.paths.append(self.path)  # type: ignore[attr-defined]
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body.encode("utf8"))

    def log_message(self, *args: object) -> None:
        """Keep the test output quiet."""


@pytest.fixture
def health_server() -> Iterator[HTTPServer]:
    """Run a fake elasticsearch health endpoint."""
    server = HTTPServer(("127.0.0.1", 0), HealthHandler)
    server.paths = []  # type: ignore[attr-defined]
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield server
    server.shutdown()
    server.server_close()


def health(status: str, *, timed_out: bool) -> str:
    """Render a cluster health response body."""
    return json.dumps({"cluster_name": "elasticsearch", "status": status, "timed_out": timed_out})


@pytest.mark.parametrize(
    "code, body, expected",
    (
        (200, health("green", timed_out=False), True),
        (200, health("yellow", timed_out=False), True),
        # documented behaviour since 8.0: a timed out wait still answers 200
        (200, health("red", timed_out=True), False),
        # behaviour observed in practice: a timed out wait answers 408
        (408, health("red", timed_out=True), False),
        (503, json.dumps({"error": {"type": "cluster_block_exception"}, "status": 503}), False),
        (200, "not json", False),
    ),
)
def test_after_start_check(
    health_server: HTTPServer, code: int, body: str, *, expected: bool
) -> None:
    """Report started only when the cluster health is at least yellow."""
    health_server.response = (code, body)  # type: ignore[attr-defined]
    executor = make_executor(port=health_server.server_address[1])
    assert executor.after_start_check() is expected
    assert health_server.paths == [ElasticSearchExecutor.HEALTH_PATH]  # type: ignore[attr-defined]


def test_after_start_check_nothing_listening() -> None:
    """Report not started when nothing answers on the port."""
    with HTTPServer(("127.0.0.1", 0), HealthHandler) as server:
        port = server.server_address[1]
    assert make_executor(port=port).after_start_check() is False
