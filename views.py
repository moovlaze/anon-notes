from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError

from schemas import NoteSchema, NoteID
from chiper import get_note_id
from db import async_session_maker, Note

router = APIRouter()

templates = Jinja2Templates("templates")
			
@router.get("/", response_class=HTMLResponse)
async def get_home_page(request: Request):
	async with async_session_maker() as session:
		stmt = select(func.count()).select_from(Note)

		result = await session.execute(stmt)
		all_notes = result.scalar()

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
	note_id = get_note_id(text=data.text, salt=data.secret)
	async with async_session_maker() as session:
		note = Note(hash=note_id, secret=data.secret, text=data.text)

		try:
			session.add(note)
			await session.commit()
		except IntegrityError as e:
			await session.rollback()
			print("ERROR:", e)
			return {"response": "failed", "msg": "Note already exists"}

	return {"response": "ok", "note_id": note_id}

@router.get('/result/{note_id}', response_class=HTMLResponse)
async def get_note(request: Request,note_id: str):
	return templates.TemplateResponse(
		request=request,
		name="hash_storage.html",
		context={
			"note_id": note_id
		}
	)

@router.post('/get_note')
async def get_note(data: NoteID):

	async with async_session_maker() as session:
		stmt = select(Note).filter_by(hash=data.note_id, secret=data.note_secret)

		result = await session.execute(stmt)
		note = result.scalar_one_or_none()

		text = note.text

		if note is None:
			return {"response": "faild", "note_final_text": "Such a note does not exist"}
		
		await session.delete(note)
		await session.commit()
		return {"response": "ok", "note_final_text": text}
		
@router.get('/note_page/{note_text}', response_class=HTMLResponse)
async def get_note_page(request: Request, note_text: str):
	return templates.TemplateResponse(
		request=request,
		name="note_page.html",
		context={
			"note_text": note_text
		}
	)