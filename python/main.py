import os
import logging
import json

from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
logger = logging.getLogger("uvicorn")
logger.level = logging.INFO


app.add_middleware(
	CORSMiddleware,
	allow_origins=[os.environ.get('FRONT_URL', 'http://localhost:3000')],
	allow_credentials=False,
	allow_methods=["GET", "POST", "PUT", "DELETE"],
	allow_headers=["*"],
)

@app.get("/")
def root():
	return PlainTextResponse(content="Hello, world!")

@app.post("/items")
def add_item(name: str = Form(...), category: str = Form(...)):
	logger.info(f"Receive item: {name}, category: {category}")

	# items.json ファイルの絶対パスを取得
	items_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "items.json")

	# items.json ファイルが存在しないか、中身が空である場合、初期化する
	if not os.path.exists(items_file_path) or os.path.getsize(items_file_path) == 0:
		# ファイルが存在しない場合、ディレクトリを作成
		os.makedirs(os.path.dirname(items_file_path), exist_ok=True)
		with open(items_file_path, "w") as f:
			json.dump({"items": []}, f)
		with open(items_file_path, "r") as f:
			data = json.load(f)

	new_item = {"name": name, "category": category}
	data["items"].append(new_item)

	with open(items_file_path, "w") as f:
		json.dump(data, f)

	return {"message": f"Item received: {name}, category: {category}"}

@app.get("/items")
def get_items():
	with open(items_file_path, "r") as f:
		data = json.load(f)
	return data
