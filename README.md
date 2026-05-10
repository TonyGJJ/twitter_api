# TwtAPI Python Demo

这是一个最小可运行的 Python Demo，用于快速调通 [TwtAPI 文档](https://www.twtapi.com/zh/docs/) 中的接口，并提供一套可复用的调用模板。

当前示例默认实现：
- `GET /api/v1/twitter/Trends`

## 1. 环境准备

建议 Python `3.10+`。

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 2. 配置 API Key

复制示例配置文件：

```bash
cp .env.example .env
```

然后编辑 `.env`，填入你自己的 Key：

```env
TWTAPI_API_KEY=你的真实key
TWTAPI_BASE_URL=https://api.twtapi.com
TWTAPI_LANG=zh
```

## 3. 运行 Demo

```bash
python -m src.main trends --woeid 1
```

输出会打印接口返回 JSON。

## 4. 常见问题

- 报错 `code=401`：通常是 `TWTAPI_API_KEY` 未设置或无效。
- 报错 `code=402`：余额不足或调用次数不足。
- 报错 `code=429`：触发限流，建议降低频率并重试。

## 5. 扩展更多接口

你可以在 `src/twtapi_client.py` 里继续添加方法，例如 `search`、`user_lookup` 等，复用同一个客户端和鉴权逻辑。
