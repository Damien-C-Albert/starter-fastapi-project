import os
from dotenv import load_dotenv

#Load environment variables from .env file
load_dotenv()

# FASTAPI configurations
HOST: str= os.environ.get("host", "localhost")
PORT: int= int(os.environ.get("port", 8000))

# Postgres configuration
PG_PORT: int= os.environ.get("PG_PORT")
PG_HOST: str= os.environ.get("PG_HOST")
PG_USERNAME: str= os.environ.get("PG_USERNAME")
PG_PASSWORD: str= os.environ.get("PG_PASSWORD")
PG_PROJECTS_DATABASE: str= os.environ.get("PG_PROJECTS_DATABASE")

PG_PROJECTS_URL = f"postgresql+asyncpg://{PG_USERNAME}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_PROJECTS_DATABASE}"


#--------------------------------------------------------------


# from dotenv import dotenv_values

## CONFIGURE YOUR ENVIRONMENT ACCORDINGLY
# ENV: str = "dev"

# if ENV not in {"dev", "test", "prod"}:
#     raise ValueError(f"Invalid ENV: {ENV}")

# ENV_FILE: str = f".env.{ENV}"

# _app_config: dict = dotenv_values(ENV_FILE)

# HOST: str = _app_config.get("HOST", "localhost")
# PORT: str = _app_config.get("PORT", 8020)


## Notes:
## - Used for control over different .env files for different cases.
## - Used in Large applications