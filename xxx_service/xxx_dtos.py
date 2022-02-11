from typing import Dict
from typing import List
from typing import Optional

from pydantic.schema import date as pydantic_date

from xxx_service.serialization_util import CamelCaseModel


################
# Incoming Dtos
################


class SomethingDto(CamelCaseModel):
    """A single something"""

    something_id: str
    something_id_datetime: pydantic_date
    something: str


class XxxServiceRequestDto(CamelCaseModel):
    """Incoming somethings saving request batch"""

    somethings: List[SomethingDto]


################
# Outgoing Dtos
################


class SomethingSavingResultDto(CamelCaseModel):
    """Result Dto for one something returned saving"""

    something_id: str


class SomethingsSavingResultDto(CamelCaseModel):
    """The somethings saved"""

    results: List[SomethingSavingResultDto]
