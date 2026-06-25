from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from contextlib import asynccontextmanager

# 모델들을 미리 로드하여 SQLModel.metadata 에 등록되게 합니다.
from app.models.user_interest import UserInterest

DATABASE_URL = "sqlite+aiosqlite:///bamsae.db"

engine = create_async_engine(DATABASE_URL, echo=True)

async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

@asynccontextmanager
async def get_session():
    """비동기 SQLModel 세션을 생성하는 컨텍스트 매니저입니다."""
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()

async def init_db():
    """데이터베이스 테이블을 비동기식으로 생성합니다."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
