"""
MCP server for the Notes app.

Shares business logic directly with api.py via notes.py — no HTTP round-trips.

Usage (stdio transport for Claude Desktop / MCP Inspector):
  python mcp_server.py
  mcp run mcp_server.py
"""

import json

from fastmcp import FastMCP

import notes

mcp = FastMCP("notes-mcp-server")


@mcp.tool()
def list_notes() -> str:
    """保存されているすべてのノートの一覧を取得する。"""
    return json.dumps(notes.list_all(), ensure_ascii=False, indent=2)


@mcp.tool()
def create_note(title: str, content: str) -> str:
    """新しいノートを作成する。

    Args:
        title: ノートのタイトル
        content: ノートの本文
    """
    return json.dumps(notes.create(title, content), ensure_ascii=False, indent=2)


@mcp.tool()
def get_note(note_id: str) -> str:
    """IDを指定してノートを取得する。

    Args:
        note_id: 取得するノートのID
    """
    note = notes.get(note_id)
    if note is None:
        return json.dumps({"error": f"Note {note_id} not found"})
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
    note = notes.update(note_id, title, content)
    if note is None:
        return json.dumps({"error": f"Note {note_id} not found"})
    return json.dumps(note, ensure_ascii=False, indent=2)


@mcp.tool()
def delete_note(note_id: str) -> str:
    """ノートを削除する。

    Args:
        note_id: 削除するノートのID
    """
    if not notes.delete(note_id):
        return json.dumps({"error": f"Note {note_id} not found"})
    return json.dumps({"deleted": note_id})


if __name__ == "__main__":
    mcp.run()
