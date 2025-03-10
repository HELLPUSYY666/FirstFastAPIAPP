from fastapi import FastAPI
from fastapi.responses import FileResponse
import os
from alembic.src.auth import router as auth_router

app = FastAPI()

app.include_router(auth_router)


@app.get('/')
def read_root():
    return {"message": "Hello world"}
