"""External web app configuration"""
import os
from pathlib import Path
from typing import Union

from dotenv import load_dotenv
from pydantic import BaseSettings


# pylint: disable=too-few-public-methods
class Settings(BaseSettings):
    """
    Main application settings,
    see https://pydantic-docs.helpmanual.io/usage/settings/#field-value-priority
    """

    resources: str = os.path.dirname(__file__) + os.sep + "resources"

    class Config:
        # pylint: disable=missing-class-docstring
        env_file = Path(__file__).parent.parent / ".env"

    # Loading env file necessary to access variable in the file
    load_dotenv(dotenv_path=Config.env_file)

    postgres_user: str = os.environ.get("POSTGRESQL_USER", "postgres")
    postgres_password: str = os.environ.get("POSTGRESQL_PASSWORD", "postgres")
    postgres_db: str = os.environ.get("DATABASE_NAME", "postgres")
    postgres_port: Union[str, int] = os.environ.get("POSTGRESQL_PORT", 5432)
    postgres_host: str = os.environ.get("POSTGRESQL_HOST", "localhost")
