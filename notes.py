import uuid

_notes: dict[str, dict] = {}


def list_all() -> list[dict]:
    return list(_notes.values())


def get(note_id: str) -> dict | None:
    return _notes.get(note_id)


def create(title: str, content: str) -> dict:
    note_id = str(uuid.uuid4())
    note = {"id": note_id, "title": title, "content": content}
    _notes[note_id] = note
    return note


def update(note_id: str, title: str | None, content: str | None) -> dict | None:
    if note_id not in _notes:
        return None
    if title is not None:
        _notes[note_id]["title"] = title
    if content is not None:
        _notes[note_id]["content"] = content
    return _notes[note_id]


def delete(note_id: str) -> bool:
    if note_id not in _notes:
        return False
    del _notes[note_id]
    return True
