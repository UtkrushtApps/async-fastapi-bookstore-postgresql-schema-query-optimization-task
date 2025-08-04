import asyncpg
import asyncio

DB_HOST = 'postgres'
DB_NAME = 'bookstore_db'
DB_USER = 'bookstore_user'
DB_PASSWORD = 'pass1234'
DB_PORT = '5432'

class Database:
    pool = None

    @classmethod
    async def init(cls):
        if not cls.pool:
            cls.pool = await asyncpg.create_pool(
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME,
                host=DB_HOST,
                port=DB_PORT,
                min_size=1,
                max_size=10
            )

    @classmethod
    async def get_conn(cls):
        if not cls.pool:
            await cls.init()
        return await cls.pool.acquire()

    @classmethod
    async def release_conn(cls, conn):
        if cls.pool:
            await cls.pool.release(conn)
