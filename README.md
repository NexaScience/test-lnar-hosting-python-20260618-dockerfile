# test-lnar-hosting-python

Notes の CRUD を提供する FastAPI サーバーと、それを MCP ツールとして公開する MCP サーバーのサンプルです。

FastAPI の `/mcp` に MCP Streamable HTTP エンドポイントをマウントしているため、**1プロセス・1ポートで REST API と MCP の両方を提供します**。

## 起動方法

### 1. 依存関係のインストール

```bash
uv sync
```

### 2. サーバーを起動

```bash
uvicorn api:app --reload
```

- REST API ドキュメント: http://localhost:8000/docs
- MCP エンドポイント: http://localhost:8000/mcp

## MCP クライアントからの接続

`supergateway` 経由で Streamable HTTP に接続する場合（lnar ダッシュボードで表示される設定）:

```json
{
  "mcpServers": {
    "test-lnar-hosting-python": {
      "command": "npx",
      "args": ["-y", "supergateway", "--streamableHttp", "http://localhost:8000/mcp"]
    }
  }
}
```

stdio transport（Claude Desktop / MCP Inspector 直接接続）を使う場合:

```bash
python mcp_server.py
```

### MCP Inspector で動作確認

```bash
npx @modelcontextprotocol/inspector python mcp_server.py
```
