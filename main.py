from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from schemas import Note, NotesList, NoteID
from chiper import get_note_id

app = FastAPI()
templates = Jinja2Templates("templates")
notes_list = NotesList()

def is_secret_exists(data: Note) -> bool:
	for note in notes_list.all_notes:
		if note.secret == data.secret:
			return True
	return False

			
@app.get("/", response_class=HTMLResponse)
async def get_home_page(request: Request):
	return templates.TemplateResponse(
		request=request,
		name="index.html",
		context={
			"notes_count": len(notes_list.all_notes),
			"page_title" : "Записки"
		}
	)

@app.post("/create_note")
async def create_note(data: Note):

	if is_secret_exists(data):
		return {"response": "faild", "msg": "write another secret phrase"}

	note_id = get_note_id(text=data.text, salt=data.secret)
	data.note_hash = note_id
	notes_list.all_notes.append(data)
	print(notes_list.all_notes)
	return {"response": "ok", "note_id": note_id}

@app.get('/result/{note_id}', response_class=HTMLResponse)
async def get_note(request: Request,note_id: str):
	return templates.TemplateResponse(
		request=request,
		name="hash_storage.html",
		context={
			"note_id": note_id
		}
	)

@app.post('/get_note')
async def get_note(data: NoteID):
	for note in notes_list.all_notes:
		if (note.note_hash == data.note_id) and (note.secret == data.note_secret):
			note_index = notes_list.all_notes.index(note)
			notes_list.all_notes.pop(note_index)
			return {"response": "ok", "note_final_text": note.text}
	return {"response": "faild", "note_final_text": "Such a note does not exist"}
		
@app.get('/note_page/{note_text}', response_class=HTMLResponse)
async def get_note_page(request: Request, note_text: str):
	return templates.TemplateResponse(
		request=request,
		name="note_page.html",
		context={
			"note_text": note_text
		}
	)