from typing import Any, Dict

from utils.http_client import APIResponse


def assert_status_code(response: APIResponse, expected_code: int) -> None:
    assert response.status_code == expected_code, (
        f"状态码校验失败，expected={expected_code}, actual={response.status_code}, body={response.text}"
    )


def assert_json_contains(response: APIResponse, expected: Dict[str, Any]) -> None:
    data = response.json()
    for key, value in expected.items():
        assert key in data, f"响应中不存在字段: {key}"
        assert data[key] == value, f"字段 {key} 值不匹配，expected={value}, actual={data[key]}"
