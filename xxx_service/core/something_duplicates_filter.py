import logging
from typing import List

import pandas as pd
from psycopg2 import Error  # type: ignore
from sqlalchemy.engine import Engine


class SomethingDuplicateFilter:
    """
    Remove all somethings that have been saved in the last 7 days - to avoid duplicates
    """

    def __init__(self, engine: Engine) -> None:
        self._engine = engine

    def _get_something_ids(self) -> List[str]:
        """Fetch all something ids of somethings that have been saved in the last 7 days"""

        con = self._engine.connect()

        something_ids = pd.DataFrame()

        try:
            something_ids = pd.read_sql(
                sql="""
                select
                    something_id
                from
                    xxx_service.something
                where
                    something_id_datetime::date >= current_date - 7
                """,
                con=con,
            )
        except Error as error:
            logging.exception(
                f"Error in {self.__class__.__name__} when fetching data.\n{error}"
            )
        finally:
            con.close()

        if something_ids.shape[0]:
            something_ids_unique = something_ids["something_id"].unique().tolist()
        else:
            something_ids_unique = []

        return [str(something_id) for something_id in something_ids_unique]

    def filter(self, something: pd.DataFrame) -> pd.DataFrame:
        """Filter the duplicate somethings"""

        something_ids_last_7_days = self._get_something_ids()
        filtered_df = something.loc[
            ~something["something_id"].isin(something_ids_last_7_days)
        ].reset_index(drop=True)

        logging.info(
            f"{something.shape[0] - filtered_df.shape[0]} from "
            f"{something.shape[0]} somethings are duplicates and will be removed."
        )
        return filtered_df
