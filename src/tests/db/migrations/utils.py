import os
from pathlib import Path
from types import SimpleNamespace

from alembic.config import Config
from alembic.script import ScriptDirectory


def make_alembic_config(cmd_opts, base_path: str) -> Config:
    if not os.path.isabs(cmd_opts.config):
        cmd_opts.config = os.path.join(base_path, cmd_opts.config)

    config = Config(file_=cmd_opts.config, ini_section=cmd_opts.name, cmd_opts=cmd_opts)

    alembic_location = str(config.get_main_option("script_location"))
    if not os.path.isabs(alembic_location):
        config.set_main_option(
            "script_location", os.path.join(base_path, alembic_location)
        )
    if cmd_opts.pg_url:
        config.set_main_option("sqlalchemy.url", cmd_opts.pg_url)

    return config


def alembic_config_from_url(pg_url) -> Config:
    """
    Provides Python object, representing alembic.ini file.
    """
    cmd_options = SimpleNamespace(
        config="alembic.ini",
        name="alembic",
        pg_url=pg_url,
        raiseerr=False,
        x=None,
    )

    alembic_base_path = str(Path(__file__).parent.parent.parent.parent.resolve())

    return make_alembic_config(cmd_options, alembic_base_path)


def get_revisions(pg_url=None):
    config = alembic_config_from_url(pg_url)

    revisions_dir = ScriptDirectory.from_config(config)

    revisions = list(revisions_dir.walk_revisions("base", "heads"))
    revisions.reverse()

    return revisions
