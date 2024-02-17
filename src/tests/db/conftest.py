import pytest
from testcontainers.postgres import PostgresContainer

from tests.db.migrations.utils import alembic_config_from_url


@pytest.fixture()
def postgres():
    with PostgresContainer("postgres:alpine") as postgres:
        postgres.driver = "asyncpg"

        yield postgres


@pytest.fixture()
def alembic_config(postgres):
    """
    Alembic configuration object, bound to temporary database.
    """
    return alembic_config_from_url(postgres.get_connection_url())
