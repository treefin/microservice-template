import datetime
import logging
from typing import Optional

import pandas as pd
from fastapi import APIRouter
from fastapi import Request

from xxx_service.xxx_dtos import XxxServiceRequestDto
from xxx_service.xxx_dtos import SomethingSavingResultDto
from xxx_service.xxx_dtos import SomethingsSavingResultDto

from xxx_service.core.something_repository import SomethingRepository  # type: ignore
from xxx_service.core.something_duplicates_filter import (
    SomethingDuplicateFilter,
)
from xxx_service.database_util import create_database_engine
from xxx_service.patterns import Singleton

xxx_service_router = APIRouter()


@xxx_service_router.post(
    "/save_somethings", response_model=SomethingsSavingResultDto
)
def save_something(
    xxx_service_request: XxxServiceRequestDto,
    request: Request,
) -> SomethingsSavingResultDto:
    """
    Something xxx endpoint - receives somethings and saves them to the DB
    """

    # create dataframe from request and perform pre-processing
    somethings = prepare_df_somethings(xxx_service_request)

    if not isinstance(somethings, pd.DataFrame):
        return SomethingsSavingResultDto(results=[])
    somethings_saving = SomethingSaving()
    result = somethings_saving.collect_data(somethings=somethings)

    # return for debugging purposes
    return SomethingsSavingResultDto(
        results=[
            SomethingSavingResultDto(something_id=something_id)
            for something_id in result["something_id"]
        ]
    )


class SomethingSaving(metaclass=Singleton):
    """Main class to handle the saving to DB process"""

    def __init__(self) -> None:
        _engine = create_database_engine()
        self._save_to_database = SomethingRepository(engine=_engine)
        self._filter_duplicate_somethings = SomethingDuplicateFilter(engine=_engine)
        logging.info(f"{self.__class__.__qualname__} class instantiated.")

    def collect_data(
        self,
        somethings: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        save somethings to DB
        """

        somethings_filtered = self._filter_duplicate_somethings.filter(
            something=somethings
        )
        self._save_to_database.save(something=somethings_filtered)

        return somethings_filtered


def prepare_df_somethings(
    somethings_xxx_request: XxxServiceRequestDto
) -> Optional[pd.DataFrame]:
    """
    Convert request into somethings dataframes
    """

    request_dict = somethings_xxx_request.dict()

    somethings = pd.DataFrame(request_dict["somethings"])

    if not somethings.shape[0]:
        return None

    return somethings
