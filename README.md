# Bookstore FastAPI — Async PostgreSQL Optimization Task

## Task Overview
A working FastAPI API for an online bookstore is suffering from slow search response times, particularly when books are queried by author or category. Users have reported delays when searching or browsing the catalog by these fields. The problem lies in a suboptimal PostgreSQL schema (lacking indexes, basic normalization) and blocking synchronous query logic within async endpoints, leading to slow user experience and inefficient resource use. You must diagnose and optimize the schema and queries to ensure the bookstore API delivers fast, concurrent search results as traffic grows.

## Guidance
- Some slow queries on endpoints that filter books by author or category due to missing indexes or poorly chosen data types.
- Synchronous psycopg2 queries used in async FastAPI endpoints may block the event loop, limiting concurrency and responsiveness.
- Missing or incomplete foreign-key relationships in schema, leaving potential for orphaned records or inconsistent data.
- Query patterns with unbounded offset/limit or full table scans reduce performance as data grows.
- Focus exclusively on PostgreSQL schema design, relationship definitions, async query logic, and optimizing for search performance.

## Database Access
- **Host**: <DROPLET_IP>
- **Port**: 5432
- **Database**: bookstore_db
- **Username**: bookstore_user
- **Password**: pass1234
- Connect with any PostgreSQL client (e.g., pgAdmin, DBeaver, psql) for inspecting schema, running EXPLAIN, or reviewing data.

## Objectives
- Redesign the book, author, and category tables with proper normalization, data types, primary and foreign key constraints.
- Create necessary single/composite indexes to enable rapid searching and filtering by author and category.
- Refactor blocking synchronous query logic to use async database access (e.g., via asyncpg) within async endpoints.
- Ensure safe, non-blocking connection management for improved concurrency.
- Demonstrate normalized relationships between books, authors, and categories in the schema.
- Achieve sub-second query response times for book search endpoints.

## How to Verify
- After completing optimizations, call GET endpoints for books by author or category and measure response (should be sub-second).
- Run EXPLAIN on primary book search queries and confirm use of indexes and efficient plans (no full scans).
- Verify referential integrity and absence of orphaned or duplicate records in the database.
- Validate that background/book-logging or similar deferred operations (if implemented) are safely executed with async DB access.
