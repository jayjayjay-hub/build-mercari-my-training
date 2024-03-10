# schemas.py

from pydantic import BaseModel, Field
from typing import List, Optional

class ItemBase(BaseModel):
	id: int = Field(..., example = 1)
	name: str = Field(..., example = "Item Name")
	category: Optional[str] = Field(..., example = "Item Category")
	image_name: Optional[str] = Field(..., example = "Image Filename")

	class Config:
		from_attribute = True
