from pydantic import BaseModel
from typing import Optional

class BookOut(BaseModel):
    id: Optional[int]
    title: str
    author: str
    category: str

class AuthorOut(BaseModel):
    id: int
    name: str

class CategoryOut(BaseModel):
    id: int
    name: str
