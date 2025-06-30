import asyncio

import uvicorn
from fastapi import FastAPI
from api.v1.views import router

from db import init_db

app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
	
	asyncio.run(init_db())
	uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
