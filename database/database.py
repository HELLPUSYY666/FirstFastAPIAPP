from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

DATABASE_URL = "postgresql+asyncpg://zakariyapolevchishikov:12345@localhost:5432/fast_api_db"

engine = create_async_engine(DATABASE_URL, echo=True)

async_session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_session_maker():
    return async_session_maker


async def get_db_session():
    async with async_session_maker() as session:
        yield session
