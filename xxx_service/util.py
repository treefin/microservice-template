from configparser import ConfigParser
from configparser import NoSectionError
from pathlib import Path
from typing import Dict

from fastapi import Request
from sqlalchemy import create_engine
from sqlalchemy.engine import Connection


def config(section: str, filename: str = "database.ini") -> Dict[str, str]:
    """Loads config for dwh"""
    file = Path(__file__).parent.parent / filename
    parser = ConfigParser()
    parser.read(file)
    if not parser.has_section(section):
        raise NoSectionError(
            f"Section {section} not found in the {filename} file"
        )
    params = parser.items(section)
    return {param[0]: param[1] for param in params}


def create_connection(stage: str) -> Connection:
    """creates a connection to dwh"""
    db_config = config(stage)
    engine = create_engine(
        f"postgresql+psycopg2://{db_config['user']}:{db_config['password']}"
        f"@{db_config['host']}/{db_config['database']}"
    )
    return engine.connect()

