import asyncio
import uuid
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from mcp_server import mcp

app = FastAPI(title="Notes API", version="1.0.0")

# MCP Streamable HTTP エンドポイントを /mcp にマウント
app.mount("/mcp", mcp.http_app(path="/"))

# In-memory storage
_notes: dict[str, dict] = {}


class NoteCreate(BaseModel):
    title: str
    content: str


class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class Note(BaseModel):
    id: str
    title: str
    content: str


@app.get("/notes", response_model=list[Note])
def list_notes():
    """ノートの一覧を返す"""
    return list(_notes.values())


@app.post("/notes", response_model=Note, status_code=201)
def create_note(body: NoteCreate):
    """新しいノートを作成する"""
    note_id = str(uuid.uuid4())
    note = {"id": note_id, "title": body.title, "content": body.content}
    _notes[note_id] = note
    return note


@app.get("/notes/{note_id}", response_model=Note)
def get_note(note_id: str):
    """IDでノートを取得する"""
    if note_id not in _notes:
        raise HTTPException(status_code=404, detail="Note not found")
    return _notes[note_id]


@app.put("/notes/{note_id}", response_model=Note)
def update_note(note_id: str, body: NoteUpdate):
    """ノートのタイトルまたは内容を更新する"""
    if note_id not in _notes:
        raise HTTPException(status_code=404, detail="Note not found")
    if body.title is not None:
        _notes[note_id]["title"] = body.title
    if body.content is not None:
        _notes[note_id]["content"] = body.content
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
        print(f"Message {i}/{max_count} at {current_time}", flush=True)
        await asyncio.sleep(1.0)
    return {"status": "done", "count": max_count}
