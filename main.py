import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from core.database import get_db
from settings import HOST, PORT


def create_app() -> FastAPI:
    app = FastAPI()
    # config cors
    # register routers
    return app

app: FastAPI= create_app()


# Application's Health check apis below:
# ------------------------------------------------------------------

@app.get("/health/app")
async def app_health_check() -> str:
    return "Yokoso(ようこそ)!"

@app.get("/health/db")
async def db_health_check(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT 1"))
    return {"db": result.scalar()}


if __name__ == "__main__":
    uvicorn.run(
        app="main:app", 
        host=HOST, 
        port=PORT, 
        reload=True
    )


# lifespan
# CORS
# api routers / Blueprints
# pydantic reqeusts validation
# loggers
# Exception handling everywhere
# jwt authentication

# Async api
# Sync api
# AI feature api, eg. recommendations etc.
# ML feature api

# done
# --------------------------
# create flask app
# dotenv configuration
# db init setup
# alembic migration
