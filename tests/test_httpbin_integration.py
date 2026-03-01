from urllib.error import URLError

import pytest

from core.assertions import assert_json_contains, assert_status_code


@pytest.mark.integration
def test_get_ip(api_client) -> None:
    try:
        response = api_client.get("/ip")
    except URLError as exc:
        pytest.skip(f"当前环境网络受限，跳过集成测试: {exc}")

    assert_status_code(response, 200)
    assert_json_contains(response, {"origin": response.json()["origin"]})
