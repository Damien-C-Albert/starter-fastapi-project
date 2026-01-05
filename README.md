# starter-fastapi-project

### Database migration: Alembic workflow
- !!! only at the very beginning while app setup, first user if multiple user purpose. first time for single user purpose.

- initialize:
    ```bash 
    alembic init alembic
    ```
- This creates ```alembic/``` folder in your root folder
- open ```alembic.ini```, configure ```sqlachemy.url``` with your DB url
- open ```alembic/env.py```, import your base and models - connects alembic to your orm and models
- Alembic does NOT auto-discover models, If you don’t ```import``` them → migrations will be wrong.
- if you are using Base to inherit DeclarativeBase, set ```target_metadata = Base.metadata```
- Enable schema support (Postgres)

    Inside ```run_migrations_online()```:

    Find:
    ```
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
    )
    ```

    Change to:
    ```
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        include_schemas=True,
    )
    ```
- Create the schema (one time)
    - Alembic does not auto-create schemas.
    - Run this manually in Postgres:
        ```
        CREATE SCHEMA IF NOT EXISTS "starter-fastapi-project";
        ```
- Generate your FIRST migration
    ```
    alembic revision --autogenerate -m "create users table"
    ```
- You can read the script in ```alembic/versions/```
- Apply the migration
    ```
    alembic upgrade head
    ```
- Migration complete, table created in db, version noted in alembic/versions/



### Normal workflow from now on (memorize this)

#### Whenever you change ORM models:
- Edit model
- Generate migration
    ```
    alembic revision --autogenerate -m "meaningful message"
    ```
- Review migration file
- Apply migration
    ```
    alembic upgrade head
    ```


### Common mistakes (so you don’t hit them)
| Mistake | Result | Prevention |
|---------|--------|-----------|
| Forgetting model import | Alembic recreates tables | Always import all models in `env.py` |
| Missing `include_schemas=True` | Tables duplicated | Add to `context.configure()` |
| Manual DB edits | Broken diffs | Use migrations for all schema changes |
| Blind autogenerate | Data loss | Review generated scripts before applying |


### Copy and replace env.py in alembic/ folder to support async database driver

if the generated file is not migrating your orm models to database table then try using the below code snippet.

I am using Postgres+asyncpg:// for this reason, my env.py was not working for alembic/ migrations.

Use the below code and it works.

```bash
import asyncio
from logging.config import fileConfig

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import Connection
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

##### !!!!!!!!!!!!!!!!!!!!!!!
##### Import your model and MetaData objects here.

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
# target_metadata = None
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations(connection: Connection) -> None:
    """Sync function that receives the underlying sync Connection."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        include_schemas=True
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode with async engine."""
    url = config.get_main_option("sqlalchemy.url")

    # Create a temporary async engine with NullPool (recommended for migrations)
    connectable = create_async_engine(
        url,
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as async_conn:
        # Bridge to sync: passes the real sync Connection to the function above
        await async_conn.run_sync(run_migrations)

    # Clean up
    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
```