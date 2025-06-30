import logging

from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, func

from chiper import get_note_id
from db import async_session_maker, Note
from api.v1.schemas import NoteSchema, NoteID

log = logging.getLogger(__name__)

async def get_notes():
	async with async_session_maker() as session:
		stmt = select(func.count()).select_from(Note)

		result = await session.execute(stmt)
		return result.scalar()

async def create_note_and_return_note_id(data: NoteSchema):
	note_id = get_note_id(text=data.text, salt=data.secret)
	async with async_session_maker() as session:
		note = Note(hash=note_id, secret=data.secret, text=data.text)

		try:
			session.add(note)
			await session.commit()
			log.info("Entry was create $s", note)
			return note_id
		except IntegrityError as e:
			await session.rollback()
			log.exception("Entry alredy exist")
			return None
		
async def get_note_text(data: NoteID):
	async with async_session_maker() as session:
		stmt = select(Note).filter_by(hash=data.note_id, secret=data.note_secret)

		result = await session.execute(stmt)
		note = result.scalar_one_or_none()

		if note is None:
			return None
		
		text = note.text
		
		await session.delete(note)
		await session.commit()
		return text