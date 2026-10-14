# API 自动化测试项目

基于 Python、Requests、Pytest 和 Postman 的 REST API 自动化测试项目，以 Restful-Booker 公共演示 API 为测试对象，覆盖预订查询、创建、修改、删除及异常场景。

## 技术栈

- Python 3.12
- Requests
- Pytest
- pytest-html
- Postman

## 测试范围

### Python + Pytest

| 模块 | 测试场景 |
|---|---|
| 预订查询 | 获取预订列表、查询单条预订 |
| 异常场景 | 查询不存在的预订、使用非法 ID |
| 预订创建 | 创建预订并校验返回字段 |
| 预订修改 | 获取 Token、修改预订并验证结果 |
| 预订删除 | 删除预订并验证资源不存在 |
| 身份认证 | 使用错误凭据验证异常响应 |

### Postman

| 请求 | 测试场景 |
|---|---|
| Get Booking List | 校验 HTTP 状态码、响应数组类型及预订 ID 字段 |
| Get Booking Details | 校验 HTTP 状态码、姓名字段及预订日期字段 |
| Get Nonexistent Booking | 校验不存在资源的 HTTP 状态码及响应体 |

Postman 集合包含 3 个请求、8 个断言，已完成一次集合运行验证。

## 环境安装

建议使用 Python 3.12 或兼容版本。

```bash
git clone https://github.com/cheeen27/restful-booker-api-tests.git
cd restful-booker-api-tests

python3 -m venv .venv
source .venv/bin/activate

python -m pip install -r requirements.txt
```

## 运行测试

运行全部 Python 自动化测试：

```bash
python -m pytest -v
```

生成 HTML 测试报告：

```bash
python -m pytest -v --html=report.html --self-contained-html
```

报告生成后，可以在 macOS 上执行：

```bash
open report.html
```

## 运行 Postman 测试

1. 下载仓库中的 `postman/exports/Restful-Booker-API-Tests.postman_collection.json`。
2. 打开 Postman，点击 **Import**，选择该 JSON 文件。
3. 打开导入的 Collection，使用 Collection Runner 运行全部请求。
4. 查看各请求的断言结果。

## 项目说明

- 使用 Requests 发送 HTTP 请求，通过 Pytest 组织测试用例并校验响应。
- 使用参数化测试覆盖多组错误认证凭据。
- 使用 Token 完成需要身份认证的预订修改和删除操作。
- 使用 Postman 编写请求级断言，补充接口手动调试与集合运行实践。
- 使用 pytest-html 生成 HTML 测试报告。
- 部分测试依赖公共演示 API 的可用性及动态测试数据，执行结果可能受外部服务影响。

本项目用于学习接口测试、自动化测试及测试报告生成，测试范围不代表已完成完整的生产级测试框架。
