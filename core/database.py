from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from settings import PG_PROJECTS_URL

# Creates engine
engine = create_async_engine(
    url=PG_PROJECTS_URL,
    echo=False, # To Reduce the logs, Used for debugging purpose
    future=True,
)

# Creates session
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Creates session when a request calls the function
# Closes the session automatically when the request is done.
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
