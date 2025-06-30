from pydantic import BaseModel

class NoteSchema(BaseModel):
	text: str
	secret: str
	note_hash: str | None = None

class NoteID(BaseModel):
	note_id: str
	note_secret: str