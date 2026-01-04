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


## Add the changes i have made in alembic to support the async driver to connect to database
