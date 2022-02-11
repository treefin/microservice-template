import logging
from threading import Lock

import pandas as pd
from psycopg2 import Error  # type: ignore
from sqlalchemy import DATE
from sqlalchemy import TEXT
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.engine import Engine

from xxx_service.database_util import save_df_to_foreign_table
from xxx_service.patterns import Singleton


class SomethingRepository(metaclass=Singleton):
    """Handle the process to save something to the database"""

    def __init__(self, engine: Engine) -> None:
        self._engine = engine
        self.dtypes = {
            "something_id": UUID,
            "something_id_datetime": DATE,
            "something": TEXT,
        }
        self.lock = Lock()

    def save(self, something: pd.DataFrame) -> None:
        """Save something to the dwh"""

        connection = self._engine.connect()
        connection_cursor = connection.connection.cursor()

        # save_df_to_foreign_table should only be used with a lock
        with self.lock:
            if something.shape[0]:
                try:
                    save_df_to_foreign_table(
                        df=something,
                        foreign_table="something",
                        schema="xxx_service",
                        connection=connection,
                        connection_cursor=connection_cursor,
                        dtypes=self.dtypes,
                    )
                except Error as error:
                    logging.exception(
                        f"Error in {self.__class__.__name__} when fetching data.\n{error}"
                    )
                finally:
                    connection_cursor.close()
                    connection.close()

            logging.info(f"{something.shape[0]} somethings have been saved.")
