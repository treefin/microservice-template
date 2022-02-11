import uuid
from typing import Dict

import pandas as pd
from psycopg2 import sql  # type: ignore
from psycopg2.extensions import cursor  # type: ignore
from sqlalchemy import create_engine
from sqlalchemy.engine import Connection
from sqlalchemy.engine import Engine

from xxx_service.config import Settings


def create_database_engine() -> Engine:
    """create engine"""

    settings: Settings = Settings()

    return create_engine(
        f"postgresql+psycopg2://{settings.postgres_user}:"
        f"{settings.postgres_password}"
        f"@{settings.postgres_host}/{settings.postgres_db}",
        pool_size=20,
        max_overflow=0,
    )


# pylint: disable=too-many-arguments
def save_df_to_foreign_table(
    df: pd.DataFrame,
    foreign_table: str,
    schema: str,
    connection: Connection,
    connection_cursor: cursor,
    dtypes: Dict,
) -> None:
    """saves dataframe to database, note: this method should be run in parallel from various threads
    working on the same foreign table, since we depend on the intermediate table to be clean"""

    # https://stackoverflow.com/questions/47429929/attributeerror-uuid-object-has-no-attribute-replace-when-using-backend-agno
    # sqlalchemy expects a string, hence, force UUIDs to str
    if df.shape[0] > 0:
        cols = df.iloc[0, :].apply(lambda x: isinstance(x, (uuid.UUID, dict)))
        df.loc[:, cols] = df.loc[:, cols].astype(str)

    # note: cstore doesn't support direct inserts, we do a 2 step process
    # pandas -> postgres table -> cstore foreign table

    # step 1. copy into the postgres table
    temp_normal_table = foreign_table + "_temp_normal_table"
    df.to_sql(
        name=temp_normal_table,
        schema=schema,
        chunksize=400000,
        con=connection,
        if_exists="append",
        dtype=dtypes,
        index=False,
    )

    # step 2. copy from postgres table table to the cstore foreign table
    copy_sql = (
        sql.SQL("select {columns} from {schema}.{table}")
        .format(
            columns=sql.SQL(", ".join(list(dtypes))),
            schema=sql.Identifier(schema),
            table=sql.Identifier(temp_normal_table),
        )
        .as_string(context=connection_cursor)
    )
    insert_statement = (
        sql.SQL("INSERT INTO {schema}.{table_name} ({columns}) {sql_query}")
        .format(
            schema=sql.Identifier(schema),
            table_name=sql.Identifier(foreign_table),
            columns=sql.SQL(", ".join(list(dtypes))),
            sql_query=sql.SQL(copy_sql),
        )
        .as_string(context=connection_cursor)
    )
    connection.execute(insert_statement)

    # step 3. truncate postgres table i.e. ensure its empty for next run
    truncate_statement = (
        sql.SQL("TRUNCATE {schema}.{table_name}")
        .format(
            schema=sql.Identifier(schema),
            table_name=sql.Identifier(temp_normal_table),
        )
        .as_string(context=connection_cursor)
    )
    connection.execute(truncate_statement)
