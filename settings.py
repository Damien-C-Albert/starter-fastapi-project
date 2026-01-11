import os
from dotenv import load_dotenv

load_dotenv()   #Load environment variables from .env file

# FASTAPI configurations
HOST: str= os.environ.get("host", "localhost")
PORT: int= int(os.environ.get("port", 8000))

# Postgres configurations
PG_PORT: int= os.environ.get("PG_PORT")
PG_HOST: str= os.environ.get("PG_HOST")
PG_USERNAME: str= os.environ.get("PG_USERNAME")
PG_PASSWORD: str= os.environ.get("PG_PASSWORD")
PG_PROJECTS_DATABASE: str= os.environ.get("PG_PROJECTS_DATABASE")

PG_PROJECTS_URL = f"postgresql+asyncpg://{PG_USERNAME}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_PROJECTS_DATABASE}"

# JWT token keys
JWT_SECRET_KEY: str = os.environ.get("JWT_SECRET_KEY")      # Secret key for signing tokens
JWT_ALGORITHM = "HS256"                                     # Algorithm used for token encoding
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 15                        # Token expiration time in minutes
