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

## エンドポイント一覧

| Method | Path | 説明 |
| ------ | ---- | ---- |
| GET    | `/health` | ヘルスチェック |
| GET    | `/notes` | ノートの一覧を取得 |
| GET    | `/notes/count` | ノートの件数を取得 |
| POST   | `/notes` | ノートを作成 |
| DELETE | `/notes` | すべてのノートを削除（0件のときは 204） |
| GET    | `/notes/{note_id}` | ノートを ID で取得 |
| PUT    | `/notes/{note_id}` | ノートを更新 |
| DELETE | `/notes/{note_id}` | ノートを削除 |
| GET    | `/stream` | ログストリーミング検証用 |

## MCP ツール一覧

| ツール名 | 説明 |
| -------- | ---- |
| `list_notes` | すべてのノートの一覧を取得 |
| `count_notes` | ノートの件数を取得 |
| `get_note` | ID を指定してノートを取得 |
| `create_note` | 新しいノートを作成 |
| `update_note` | ノートのタイトル/本文を更新 |
| `delete_note` | ノートを ID で削除 |
| `delete_all_notes` | すべてのノートを一括削除 |

## curl での動作確認

```bash
# ノート作成
curl -s -X POST http://localhost:8000/notes \
  -H 'Content-Type: application/json' \
  -d '{"title": "memo", "content": "hello"}'

# 一覧取得
curl -s http://localhost:8000/notes

# 件数取得
curl -s http://localhost:8000/notes/count

# 一括削除（0件のときは 204 No Content が返る）
curl -i -X DELETE http://localhost:8000/notes
```

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
