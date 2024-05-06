import os

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.database.models import Base

# ORM SQLAlchemy
engine = create_async_engine(os.getenv('DBURL'), echo=True)

session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)