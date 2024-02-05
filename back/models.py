# models.py

from sqlalchemy import Column, String, Integer
from .database import Base

class Item(Base):
	__tablename__ = "items"

	id = Column(Integer, primary_key = True, index = True)
	name = Column(String, index = True)
	category = Column(String, index = True)
	image_name = Column(String, index = True)
