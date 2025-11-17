import os
import asyncpg
from dotenv import load_dotenv

load_dotenv()
DB_URL = os.getenv("DATABASE_URL")

async def get_db_connection():
    return await asyncpg.connect(DB_URL)

async def search_culture_db(embedding_vector):
    """Finds the 3 most relevant database records for a given vector."""
    conn = await get_db_connection()
    try:
        # <=> is the distance operator in pgvector
        rows = await conn.fetch("""
            SELECT title, content, media_url 
            FROM heritage_items 
            ORDER BY embedding <=> $1 ASC 
            LIMIT 3
        """, str(embedding_vector))
        return [dict(row) for row in rows]
    finally:
        await conn.close()