from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.http_client import APIClient


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--run-integration",
        action="store_true",
        default=False,
        help="是否执行依赖外部网络的集成测试",
    )


@pytest.fixture(scope="session")
def api_client() -> APIClient:
    return APIClient()


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    if config.getoption("--run-integration"):
        return

    skip_integration = pytest.mark.skip(reason="需要 --run-integration 参数才执行")
    for item in items:
        if "integration" in item.keywords:
            item.add_marker(skip_integration)
