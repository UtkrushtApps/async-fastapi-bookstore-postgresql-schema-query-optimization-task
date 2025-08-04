from fastapi import APIRouter, HTTPException
from app.database import Database
from app.schemas.schemas import BookOut, AuthorOut, CategoryOut
from typing import List

router = APIRouter()

@router.get("/books", response_model=List[BookOut])
async def get_books(author: str = None, category: str = None):
    conn = await Database.get_conn()
    try:
        query = "SELECT b.id, b.title, a.name, c.name FROM books b JOIN authors a ON b.author_id=a.id JOIN categories c ON b.category_id=c.id"
        values = []
        if author and category:
            query += " WHERE a.name ILIKE $1 AND c.name ILIKE $2"
            values += [f"%{author}%", f"%{category}%"]
        elif author:
            query += " WHERE a.name ILIKE $1"
            values.append(f"%{author}%")
        elif category:
            query += " WHERE c.name ILIKE $1"
            values.append(f"%{category}%")
        # Inefficient: no indexes on a.name or c.name; large scan
        rows = await conn.fetch(query, *values)
        return [BookOut(id=r[0], title=r[1], author=r[2], category=r[3]) for r in rows]
    finally:
        await Database.release_conn(conn)

@router.post("/books", response_model=BookOut)
async def add_book(book: BookOut):
    conn = await Database.get_conn()
    try:
        # Inefficient: author/category looked up each time
        author_id = await conn.fetchval("SELECT id FROM authors WHERE name=$1", book.author)
        if not author_id:
            raise HTTPException(status_code=400, detail="Author not found")
        category_id = await conn.fetchval("SELECT id FROM categories WHERE name=$1", book.category)
        if not category_id:
            raise HTTPException(status_code=400, detail="Category not found")
        book_id = await conn.fetchval("INSERT INTO books (title, author_id, category_id) VALUES ($1, $2, $3) RETURNING id", book.title, author_id, category_id)
        return BookOut(id=book_id, title=book.title, author=book.author, category=book.category)
    finally:
        await Database.release_conn(conn)

@router.get("/authors", response_model=List[AuthorOut])
async def list_authors():
    conn = await Database.get_conn()
    try:
        rows = await conn.fetch("SELECT id, name FROM authors")
        return [AuthorOut(id=r[0], name=r[1]) for r in rows]
    finally:
        await Database.release_conn(conn)

@router.get("/categories", response_model=List[CategoryOut])
async def list_categories():
    conn = await Database.get_conn()
    try:
        rows = await conn.fetch("SELECT id, name FROM categories")
        return [CategoryOut(id=r[0], name=r[1]) for r in rows]
    finally:
        await Database.release_conn(conn)
