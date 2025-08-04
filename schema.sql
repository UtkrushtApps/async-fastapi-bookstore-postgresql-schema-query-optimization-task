-- Non-normalized/scaled-down tables, missing indexes and constraints
DROP TABLE IF EXISTS books CASCADE;
DROP TABLE IF EXISTS authors CASCADE;
DROP TABLE IF EXISTS categories CASCADE;

CREATE TABLE authors (
    id SERIAL PRIMARY KEY,
    name TEXT -- No unique constraint
);

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name TEXT -- No unique constraint
);

CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    title TEXT,
    author_id INTEGER, -- No foreign key constraint
    category_id INTEGER -- No foreign key constraint
    -- Missing index on title, author_id, category_id
);
