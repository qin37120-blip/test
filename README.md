# Python 接口自动化工程模板

这是一个可直接运行的 Python 接口自动化项目，基于 `pytest`，内置：

- 统一 HTTP 客户端封装（标准库实现）
- 配置管理（JSON）
- 日志输出
- 断言工具
- 单元测试 + 可选集成测试
- CI（GitHub Actions）示例

## 目录结构

```text
.
├── config/
│   └── settings.json
├── core/
│   └── assertions.py
├── tests/
│   ├── conftest.py
│   ├── test_api_client_unit.py
│   └── test_httpbin_integration.py
├── utils/
│   ├── http_client.py
│   └── logger.py
├── .github/
│   └── workflows/
│       └── ci.yml
├── pytest.ini
├── requirements.txt
└── README.md
```

## 1. 安装依赖

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 2. 运行测试

默认仅运行离线单元测试（不会访问外网）：

```bash
pytest
```

运行集成测试（会访问 `https://httpbin.org`）：

```bash
pytest --run-integration
```

## 3. 配置说明

`config/settings.json`：

- `env`: 当前环境名
- `base_url`: 默认接口地址
- `timeout`: 超时时间（秒）

你也可以通过环境变量 `BASE_URL` 覆盖 `base_url`。
