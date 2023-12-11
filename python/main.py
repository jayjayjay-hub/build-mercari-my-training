import os
import logging
import json
import hashlib

from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI, Form, HTTPException, UploadFile, File, Path
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware

# main.py が存在するディレクトリの絶対パスを取得
current_dir = os.path.dirname(os.path.realpath(__file__))

# データベースファイルの絶対パスを取得
database_path = os.path.abspath(os.path.join(current_dir, '..', 'db', 'items.db'))

# SQLite db path
database_url = f"sqlite:///{database_path}"

# SQLAlchemy engine
engine = create_engine(database_url)

# SQLAlchemy metadata
metadata = MetaData()

# items table
items = Table(
	"items",
	metadata,
	Column("id", Integer, primary_key = True, index = True),
	Column("name", String, index = True),
	Column("category", String, index = True),
	Column("image_name", String, index = True),
)

# create table
metadata.create_all(engine)

app = FastAPI()
logger = logging.getLogger("uvicorn")
logger.level = logging.INFO

# items.json ファイルの絶対パスを取得
items_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "items.json")

# images ディレクトリの絶対パスを取得
images_folder_path =  os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")

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
def add_item(name: str = Form(...), category: str = Form(...), image: UploadFile = File(...)):
	logger.info(f"Receive item: {name}, category: {category}")

	# items.json ファイルが存在しないか、中身が空である場合、初期化する
	if not os.path.exists(items_file_path) or os.path.getsize(items_file_path) == 0:
		# ファイルが存在しない場合、ディレクトリを作成
		os.makedirs(os.path.dirname(items_file_path), exist_ok=True)
		with open(items_file_path, "w") as f:
			json.dump({"items": []}, f)
	with open(items_file_path, "r") as f:
			data = json.load(f)

	# ファイルのハッシュを計算してファイル名を作成
	file_content = image.file.read()
	image_hash = hashlib.sha256(file_content).hexdigest()
	image_filename = f"{image_hash}.jpg"

	# 画像を保存
	image_path = os.path.join(images_folder_path, image_filename)
	with open(image_path, "wb") as f:
		f.write(file_content)

	# SQLAlchemy session を作成
	SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
	db = SessionLocal()

	# itemsテーブルにデータを追加
	db.execute(
		items.insert().values(
			name = name,
			category = category,
			image_name = image_filename,
		)
	)

	# セッションのコミット
	db.commit()

	# セッションのクローズ
	db.close()

	return {"message": f"Item received: {name}, category: {category}, image: {image_filename}"}

@app.get("/items")
def get_items():
	# SQLAlchemy session を作成
	SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
	db = SessionLocal()

	# itemsテーブルからデータを取得
	result = db.query(items).all()

	# セッションのクローズ
	db.close()

	# 結果をリストに変換
	items_list = [{"id": row.id, "name": row.name, "category": row.category, "image_name": row.image_name} for row in result]

	return {"items": items_list}

@app.get("/items/{item_id}")
def get_item(item_id: int = Path(..., title="The ID of the item to get")):
	# SQLAlchemy session を作成
	SessionLocal = sessionmaker(aoutocommit=False, outoflush=False, bind=engine)
	db = SessionLocal()

	# itemsテーブルから特定のデータを取得
	result = db.query(items).filter(items.c.id == item_id).first()

	# セッションのクローズ
	db.close()

	# item_id に対応する商品が存在するか確認
	if not result:
		raise HTTPException(status_code=404, detail="Item not found")

	return {"id": result.id, "name": result.name, "category": result.category, "image_name": result.image_name}
