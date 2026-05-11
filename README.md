# TwtAPI Official Python Demo (Flask)

这是 TwtAPI 官方 Python 示例仓库（Flask 版），目标是：
- 让开发者 3 分钟内跑通 TwtAPI
- 提供可直接复用的 Python 客户端结构
- 同时支持「网页交互 Demo」和「CLI 调用示例」

文档地址：
- [TwtAPI API 文档](https://www.twtapi.com/zh/docs/)

当前已内置示例接口：
- `GET /api/v1/twitter/Trends`
- `GET /api/v1/twitter/Search`
- `GET /api/v1/twitter/UserResultByScreenName`
- `GET /api/v1/twitter/TweetDetail`

## 1. 环境准备

建议 Python `3.9+`。

```bash
python3 -m venv venv
source venv/bin/activate
venv/bin/pip install -r requirements.txt
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

启动 Flask 页面 Demo：

```bash
python app.py
```

浏览器访问：

```text
http://127.0.0.1:5000
```

CLI 示例（可选）：

```bash
python -m src.main trends --woeid 1
python -m src.main search --q "bitcoin" --type Top --count 20
python -m src.main user --username "solana"
python -m src.main tweet-detail --tweet-id "1768778186186195177"
```

输出会打印接口返回 JSON；网页端会直接展示返回体。

## 4. 常见问题

- 报错 `code=401`：通常是 `TWTAPI_API_KEY` 未设置或无效。
- 报错 `code=402`：余额不足或调用次数不足。
- 报错 `code=429`：触发限流，建议降低频率并做重试退避。

## 5. 项目结构

```text
twtapi_demo/
├── app.py                  # Flask 入口与 demo 路由
├── templates/index.html    # 网页示例
├── src/
│   ├── config.py           # 环境变量配置
│   ├── twtapi_client.py    # TwtAPI 客户端封装
│   └── main.py             # CLI 示例入口
└── .env.example
```
