"""Extending marshmallows (serialization/deserialization/validation) functionality"""
from pydantic import BaseModel


def snake_case_to_camelcase(field_name: str) -> str:
    """Converts snake case to camelcase"""
    parts = iter(field_name.split("_"))
    return next(parts) + "".join(i.title() for i in parts)


class CamelCaseModel(BaseModel):
    """Camelcase fields ofs Pydantic Models"""

    class Config:
        """Config"""

        alias_generator = snake_case_to_camelcase
        allow_population_by_field_name = True
