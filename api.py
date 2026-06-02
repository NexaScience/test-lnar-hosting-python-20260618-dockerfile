import asyncio
import uuid
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel

from mcp_server import mcp

# FastMCP の Streamable HTTP アプリ。`path="/"` にすることで、`/mcp` に
# マウントしたときに最終 URL が `/mcp/` で到達できる。
_mcp_app = mcp.http_app(path="/")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # FastMCP の StreamableHTTPSessionManager は親 ASGI の lifespan で
    # 初期化される。これを伝搬しないと POST /mcp/ が
    # "task group was not initialized" で 500 になる。
    async with _mcp_app.lifespan(app):
        yield


app = FastAPI(title="Notes API", version="1.0.0", lifespan=lifespan)

# MCP Streamable HTTP エンドポイントを /mcp にマウント
app.mount("/mcp", _mcp_app)

# In-memory storage
_notes: dict[str, dict] = {}


@app.get("/health")
def health():
    """ヘルスチェック用エンドポイント"""
    return {"status": "ok"}


@app.get("/version")
def version():
    """API のバージョン情報を返す"""
    return {"name": app.title, "version": app.version}


class NoteCreate(BaseModel):
    title: str
    content: str
    tags: list[str] = []


class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[list[str]] = None


class Note(BaseModel):
    id: str
    title: str
    content: str
    tags: list[str] = []


@app.get("/notes", response_model=list[Note])
def list_notes(tag: Optional[str] = None):
    """ノートの一覧を返す。`tag` を指定するとそのタグを持つノートのみを返す。"""
    notes = list(_notes.values())
    if tag is not None:
        notes = [n for n in notes if tag in n.get("tags", [])]
    return notes


@app.get("/notes/count")
def count_notes():
    """保存されているノートの件数を返す"""
    return {"count": len(_notes)}


@app.get("/notes/tags", response_model=list[str])
def list_tags():
    """全ノートに付与されているタグの一覧を重複なし・昇順で返す"""
    seen: set[str] = set()
    for note in _notes.values():
        seen.update(note.get("tags", []))
    return sorted(seen)


@app.post("/notes", response_model=Note, status_code=201)
def create_note(body: NoteCreate):
    """新しいノートを作成する"""
    note_id = str(uuid.uuid4())
    note = {
        "id": note_id,
        "title": body.title,
        "content": body.content,
        "tags": list(body.tags),
    }
    _notes[note_id] = note
    return note


@app.delete("/notes")
def delete_all_notes():
    """すべてのノートを削除する。

    0件のときは 204 No Content、それ以外は削除件数を返す。
    """
    deleted = len(_notes)
    if deleted == 0:
        return Response(status_code=204)
    _notes.clear()
    return {"deleted": deleted}


@app.get("/notes/{note_id}", response_model=Note)
def get_note(note_id: str):
    """IDでノートを取得する"""
    if note_id not in _notes:
        raise HTTPException(status_code=404, detail="Note not found")
    return _notes[note_id]


@app.put("/notes/{note_id}", response_model=Note)
def update_note(note_id: str, body: NoteUpdate):
    """ノートのタイトル、内容、またはタグを更新する"""
    if note_id not in _notes:
        raise HTTPException(status_code=404, detail="Note not found")
    if body.title is not None:
        _notes[note_id]["title"] = body.title
    if body.content is not None:
        _notes[note_id]["content"] = body.content
    if body.tags is not None:
        _notes[note_id]["tags"] = list(body.tags)
    return _notes[note_id]


@app.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: str):
    """ノートを削除する"""
    if note_id not in _notes:
        raise HTTPException(status_code=404, detail="Note not found")
    del _notes[note_id]


@app.get("/stream")
async def stream(max_count: int = 10):
    """
    lnar log streaming 検証用エンドポイント。
    1秒ごとに stdout に print する。HTTP レスポンスは print 完了後に返る。
    """
    for i in range(1, max_count + 1):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Message {i}/{max_count} at {current_time}")
        await asyncio.sleep(1.0)
    return {"status": "done", "count": max_count}
