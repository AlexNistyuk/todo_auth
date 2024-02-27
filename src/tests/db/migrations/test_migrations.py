import pytest
from alembic.command import downgrade, upgrade
from alembic.config import Config
from alembic.script import Script

from tests.db.migrations.utils import get_revisions


@pytest.mark.parametrize("revision", get_revisions())
def test_migrations(alembic_config: Config, revision: Script):
    upgrade(alembic_config, revision.revision)

    down_revision = "-1" if not (x := revision.down_revision) else str(x)

    downgrade(alembic_config, down_revision)
    upgrade(alembic_config, revision.revision)
