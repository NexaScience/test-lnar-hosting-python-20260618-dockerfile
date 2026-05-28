"""
MCP server that wraps the Notes REST API.

Usage:
  1. Start the FastAPI server:   uvicorn api:app --reload
  2. Start this MCP server:      python mcp_server.py
     or via stdio transport:     mcp run mcp_server.py
"""

import json
import os

import httpx
from fastmcp import FastMCP

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

mcp = FastMCP("notes-mcp-server")


def _get(path: str) -> dict | list:
    with httpx.Client() as client:
        r = client.get(f"{API_BASE_URL}{path}")
        r.raise_for_status()
        return r.json()


def _post(path: str, payload: dict) -> dict:
    with httpx.Client() as client:
        r = client.post(f"{API_BASE_URL}{path}", json=payload)
        r.raise_for_status()
        return r.json()


def _put(path: str, payload: dict) -> dict:
    with httpx.Client() as client:
        r = client.put(f"{API_BASE_URL}{path}", json=payload)
        r.raise_for_status()
        return r.json()


def _delete(path: str) -> None:
    with httpx.Client() as client:
        r = client.delete(f"{API_BASE_URL}{path}")
        r.raise_for_status()


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------


@mcp.tool()
def list_notes() -> str:
    """保存されているすべてのノートの一覧を取得する。"""
    notes = _get("/notes")
    return json.dumps(notes, ensure_ascii=False, indent=2)


@mcp.tool()
def create_note(title: str, content: str) -> str:
    """新しいノートを作成する。

    Args:
        title: ノートのタイトル
        content: ノートの本文
    """
    note = _post("/notes", {"title": title, "content": content})
    return json.dumps(note, ensure_ascii=False, indent=2)


@mcp.tool()
def get_note(note_id: str) -> str:
    """IDを指定してノートを取得する。

    Args:
        note_id: 取得するノートのID
    """
    note = _get(f"/notes/{note_id}")
    return json.dumps(note, ensure_ascii=False, indent=2)


@mcp.tool()
def update_note(
    note_id: str,
    title: str | None = None,
    content: str | None = None,
) -> str:
    """ノートのタイトルまたは本文を更新する。

    Args:
        note_id: 更新するノートのID
        title: 新しいタイトル（省略可）
        content: 新しい本文（省略可）
    """
    payload = {k: v for k, v in {"title": title, "content": content}.items() if v is not None}
    note = _put(f"/notes/{note_id}", payload)
    return json.dumps(note, ensure_ascii=False, indent=2)


@mcp.tool()
def delete_note(note_id: str) -> str:
    """ノートを削除する。

    Args:
        note_id: 削除するノートのID
    """
    _delete(f"/notes/{note_id}")
    return f"Note {note_id} deleted successfully."


@mcp.tool()
def get_greeting(name: str = "world") -> str:
    """環境変数 GREETING を使って挨拶メッセージを取得する。

    Args:
        name: 挨拶を向ける相手の名前（省略時は "world"）
    """
    result = _get("/greeting", params={"name": name})
    return json.dumps(result, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    mcp.run()
