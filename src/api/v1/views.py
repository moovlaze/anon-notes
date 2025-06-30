from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from settings import BASE_DIR
from .schemas import NoteSchema, NoteID
from services.notes import create_note_and_return_note_id, get_note_text, get_notes

router = APIRouter()

templates = Jinja2Templates(BASE_DIR / "templates")
			
@router.get("/", response_class=HTMLResponse)
async def get_home_page(request: Request):
	all_notes = await get_notes()

	return templates.TemplateResponse(
		request=request,
		name="index.html",
		context={
			"notes_count": all_notes,
			"page_title" : "Записки"
		}
	)

@router.post("/create_note")
async def create_note(data: NoteSchema):	
	note_id = await create_note_and_return_note_id(data=data)

	if note_id is None:
		return {"response": "failed", "msg": "Note already exists"}

	return {"response": "ok", "note_id": note_id}


@router.post('/get_note')
async def get_note(data: NoteID):
	text = await get_note_text(data=data)

	if text is None:
		return {"response": "failed", "note_final_text": "Such a note does not exist"}
	
	return {"response": "ok", "note_final_text": text}
		
@router.get('/result/{note_id}', response_class=HTMLResponse)
async def get_note(request: Request,note_id: str):
	return templates.TemplateResponse(
		request=request,
		name="hash_storage.html",
		context={
			"note_id": note_id
		}
	)

@router.get('/note_page/{note_text}', response_class=HTMLResponse)
async def get_note_page(request: Request, note_text: str):
	return templates.TemplateResponse(
		request=request,
		name="note_page.html",
		context={
			"note_text": note_text
		}
	)