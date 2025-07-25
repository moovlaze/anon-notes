import logging

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from settings import DEBUG

log = logging.getLogger(__name__)

class Base(DeclarativeBase):
	pass

class Note(Base):
	__tablename__ = "notes"

	hash: Mapped[str] = mapped_column(primary_key=True)
	secret: Mapped[str]
	text: Mapped[str]

async_engine = create_async_engine(url="postgresql+asyncpg://postgres:postgres@db-anon-notes:5432/postgres", echo=DEBUG)
async_session_maker = async_sessionmaker(bind=async_engine)

async def init_db():
	log.info("start init db")
	async with async_engine.begin() as conn:
		await conn.run_sync(Base.metadata.drop_all)
		await conn.run_sync(Base.metadata.create_all)
	log.info("finish init db")
	

