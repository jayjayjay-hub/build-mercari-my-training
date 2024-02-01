# main.py

import os
import logging
from typing import Optional

from fastapi import FastAPI, Form, HTTPException, UploadFile, File, Path, Depends, Response, status
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic
from sqlalchemy.orm import Session

from . import models, schemas, crud
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

security = HTTPBasic()
logger = logging.getLogger("uvicorn")
logger.level = logging.INFO

app.add_middleware(
	CORSMiddleware,
	allow_origins=[os.environ.get('FRONT_URL', 'http://localhost:3000')],
	allow_credentials=False,
	allow_methods=["GET", "POST", "PUT", "DELETE"],
	allow_headers=["*"],
)

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

@app.get("/")
async def root():
	return PlainTextResponse(content="Hello, world!")

@app.get("/items")
async def get_items(db: Session = Depends(get_db)):
	return crud.get_items(db=db)

@app.get("/items/{item_id}")
async def get_item(item_id: int = Path(..., title="The ID of the item to get"), db: Session = Depends(get_db)):
	return crud.get_item_by_id(item_id, db)

@app.get("/search")
async def search_items(keyword: str, db: Session = Depends(get_db)):
	return crud.get_item_by_keyword(keyword, db)

@app.post("/items")
async def add_item(
	name: str = Form(...),
	category: str = Form(...),
	image: UploadFile = File(None),
	db: Session = Depends(get_db)
	):
	logger.info(f"Receive item: {name}, category: {category}")
	return crud.post_item(
		name=name,
		category=category,
		image=image,
		db=db
		)

@app.delete("/items/delete/{item_id}")
async def delete_item(item_id: int = Path(..., title="The ID of the item to delete"), db: Session = Depends(get_db)):
	return crud.delete_item_by_id(item_id, db)
