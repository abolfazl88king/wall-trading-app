from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Database URL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/wall.db")

# Convert to async SQLite URL
if DATABASE_URL.startswith("sqlite:///"):
    async_database_url = DATABASE_URL.replace("sqlite://", "sqlite+aiosqlite:///")
else:
    async_database_url = DATABASE_URL

# Create database directory
if DATABASE_URL.startswith("sqlite"):
    db_path = Path(DATABASE_URL.replace("sqlite:///", "")).parent
    db_path.mkdir(parents=True, exist_ok=True)

# Create async engine
engine = create_async_engine(
    async_database_url,
    echo=os.getenv("DATABASE_ECHO", "False") == "True",
    future=True,
    connect_args={"check_same_thread": False} if "sqlite" in async_database_url else {},
    poolclass=StaticPool if "sqlite" in async_database_url else None,
)

# Create session factory
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Base class for models
Base = declarative_base()

async def get_db():
    """Dependency to get DB session"""
    async with AsyncSessionLocal() as session:
        yield session

async def init_db():
    """Initialize database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
