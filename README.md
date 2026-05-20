# test-lnar-hosting-python

Notes の CRUD を提供する FastAPI サーバーと MCP サーバーのサンプルです。

## アーキテクチャ

```
notes.py          ← ビジネスロジック（共有）
  ├── api.py      ← FastAPI REST エンドポイント (/notes)
  └── mcp_server.py ← MCP ツール (/mcp)
```

REST と MCP はどちらも `notes.py` のロジックを直接呼ぶため、HTTP 経由の自己呼び出しが発生しません。1プロセス・1ポートで REST API と MCP Streamable HTTP の両方を提供します。

## 起動方法

```bash
uv sync
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
