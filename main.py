import asyncio

import uvicorn
from fastapi import FastAPI
from views import router

from db import init_db

app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
	asyncio.run(init_db())
	uvicorn.run(app="main:app", reload=True)
