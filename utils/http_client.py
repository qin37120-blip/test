import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional
from urllib import parse, request

from utils.logger import get_logger

LOGGER = get_logger(__name__)
CONFIG_PATH = Path(__file__).resolve().parents[1] / "config" / "settings.json"


@dataclass
class APIResponse:
    status_code: int
    text: str
    headers: Dict[str, str]

    def json(self) -> Dict[str, Any]:
        return json.loads(self.text)


class UrllibSession:
    """使用 urllib 发起请求。"""

    def request(
        self,
        method: str,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 10,
        **kwargs: Any,
    ) -> APIResponse:
        params = kwargs.pop("params", None)
        json_body = kwargs.pop("json", None)

        if params:
            query = parse.urlencode(params)
            separator = "&" if "?" in url else "?"
            url = f"{url}{separator}{query}"

        data = None
        request_headers = headers.copy() if headers else {}
        if json_body is not None:
            data = json.dumps(json_body).encode("utf-8")
            request_headers.setdefault("Content-Type", "application/json")

        req = request.Request(url=url, data=data, headers=request_headers, method=method)
        with request.urlopen(req, timeout=timeout) as resp:
            text = resp.read().decode("utf-8")
            return APIResponse(
                status_code=resp.getcode(),
                text=text,
                headers=dict(resp.headers.items()),
            )


def load_config(config_path: Path = CONFIG_PATH) -> Dict[str, Any]:
    """读取 JSON 配置。"""
    with open(config_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, dict):
        raise ValueError("配置文件格式错误，必须是字典结构")

    return data


class APIClient:
    """简单 API 客户端，封装常见请求方法。"""

    def __init__(
        self,
        base_url: Optional[str] = None,
        timeout: Optional[int] = None,
        session: Optional[Any] = None,
    ) -> None:
        config = load_config()
        self.base_url = (base_url or os.getenv("BASE_URL") or config["base_url"]).rstrip("/")
        self.timeout = timeout or config.get("timeout", 10)
        self.session = session or UrllibSession()

    def request(
        self,
        method: str,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None,
        **kwargs: Any,
    ) -> APIResponse:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        LOGGER.info("%s %s", method.upper(), url)
        response = self.session.request(
            method=method.upper(),
            url=url,
            headers=headers,
            timeout=self.timeout,
            **kwargs,
        )
        LOGGER.info("Response status: %s", response.status_code)
        return response

    def get(self, endpoint: str, **kwargs: Any) -> APIResponse:
        return self.request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs: Any) -> APIResponse:
        return self.request("POST", endpoint, **kwargs)
