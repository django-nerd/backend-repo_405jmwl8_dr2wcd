import os
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("database")
logging.basicConfig(level=logging.INFO)

DB_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DATABASE_NAME", "appdb")

_client: Optional[AsyncIOMotorClient] = None
_db: Optional[AsyncIOMotorDatabase] = None

async def get_client() -> AsyncIOMotorClient:
    global _client
    if _client is None:
        logger.info("Connecting to MongoDB at %s", DB_URL)
        _client = AsyncIOMotorClient(DB_URL)
    return _client

async def get_db() -> AsyncIOMotorDatabase:
    global _db
    if _db is None:
        client = await get_client()
        _db = client[DB_NAME]
    return _db

async def create_document(collection: str, data: Dict[str, Any]) -> str:
    db = await get_db()
    doc = {**data, "created_at": datetime.utcnow(), "updated_at": datetime.utcnow()}
    res = await db[collection].insert_one(doc)
    return str(res.inserted_id)

async def get_documents(collection: str, filter_dict: Optional[Dict[str, Any]] = None, limit: int = 50) -> List[Dict[str, Any]]:
    db = await get_db()
    cursor = db[collection].find(filter_dict or {}).limit(limit)
    items: List[Dict[str, Any]] = []
    async for doc in cursor:
        doc["_id"] = str(doc.get("_id"))
        items.append(doc)
    return items
