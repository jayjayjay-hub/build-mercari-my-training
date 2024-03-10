# crud.py

import os
import json
import hashlib

from sqlalchemy.orm import Session

from . import models
from . import schemas
from fastapi import UploadFile, status, Response, HTTPException

items_file_path = "../../db/items.json"
images_folder_path = "images/"

def post_item(name: str, category: str, image: UploadFile, db: Session):
	if image:
		image_filename = image.filename
		# ファイルのハッシュを計算してファイル名を作成
		file_content = image.file.read()
		image_hash = hashlib.sha256(file_content).hexdigest()
		image_filename = f"{image_hash}.jpg"

		# 画像を保存
		image_path = os.path.join(images_folder_path, image_filename)
		with open(image_path, "wb") as f:
			f.write(file_content)
	else:
		image_filename = None

	item = models.Item(name = name, category = category, image_name = image_filename)
	# items.json ファイルが存在しないか、中身が空である場合、初期化する
	if not os.path.exists(items_file_path) or os.path.getsize(items_file_path) == 0:
		# ファイルが存在しない場合、ディレクトリを作成
		os.makedirs(os.path.dirname(items_file_path), exist_ok=True)
		with open(items_file_path, "w") as f:
			json.dump({"items": []}, f)
	with open(items_file_path, "r") as f:
			data = json.load(f)


	# itemsテーブルにデータを追加
	db.add(item)

	# セッションのコミット
	db.commit()

	# セッションのクローズ
	db.close()

	return {"message": f"Item received: {name}, category: {category}, image: {image_filename}"}

def get_items(db: Session):
	items = db.query(models.Item).all()
	return items

def get_item_by_id(item_id: int, db: Session):
	item = db.query(models.Item).filter(models.Item.id == item_id).first()
	if item is None:
		raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Item not found")
	return item

def get_item_by_keyword(keyword: str, db: Session):
	items = db.query(models.Item).filter(models.Item.name.like(f"%{keyword}%")).all()
	if items is None:
		raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Item not found")
	return items

def delete_item_by_id(item_id: int, db: Session):
	item = db.query(models.Item).filter(models.Item.id == item_id).first()
	if item is None:
		raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Item not found")
	db.delete(item)
	db.commit()
	return item
