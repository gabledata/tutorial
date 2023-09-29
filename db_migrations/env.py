from logging.config import fileConfig

from alembic import context
from sqlalchemy import URL, create_engine, pool


config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


target_metadata = None


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = URL.create(
        drivername="postgresql+psycopg2",
        username="postgres",
        password="postgres",
        host="localhost",
        port=5432,
        database="tutorial",
    )
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    db_client = create_engine(
        URL.create(
            drivername="postgresql+psycopg2",
            username="postgres",
            password="postgres",
            host="0.0.0.0",
            port=5432,
            database="tutorial",
        )
    )

    with db_client.engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
