from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import notes
from mcp_server import mcp

_mcp_app = mcp.http_app(path="/")


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with _mcp_app.lifespan(app):
        yield


app = FastAPI(title="Notes API", version="1.0.0", lifespan=lifespan)

# MCP Streamable HTTP エンドポイントを /mcp にマウント
app.mount("/mcp", _mcp_app)


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
    return notes.list_all()


@app.post("/notes", response_model=Note, status_code=201)
def create_note(body: NoteCreate):
    """新しいノートを作成する"""
    return notes.create(body.title, body.content)


@app.get("/notes/{note_id}", response_model=Note)
def get_note(note_id: str):
    """IDでノートを取得する"""
    note = notes.get(note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@app.put("/notes/{note_id}", response_model=Note)
def update_note(note_id: str, body: NoteUpdate):
    """ノートのタイトルまたは内容を更新する"""
    note = notes.update(note_id, body.title, body.content)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@app.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: str):
    """ノートを削除する"""
    if not notes.delete(note_id):
        raise HTTPException(status_code=404, detail="Note not found")
