import datetime
import json
import uuid
from pathlib import Path

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import parse_obj_as
from starlette.testclient import TestClient

from xxx_service import init
from xxx_service.xxx_dtos import XxxServiceRequestDto
from xxx_service.xxx_dtos import SomethingDto
from xxx_service.xxx_dtos import SomethingsSavingResultDto

app = FastAPI()

RESOURCES_PATH: Path = Path(__file__).parent / "resources"


@app.on_event("startup")
def startup_event() -> None:
    """startup"""
    init(app)


def test_save_somethings() -> None:
    """Test saving somethings"""

    with TestClient(app) as client:
        u1 = SomethingDto(
            something_id=str(uuid.uuid4()),
            event_id_datetime=datetime.datetime.now(),
            something="some type",
        )
        u2 = SomethingDto(
            something_id=str(uuid.uuid4()),
            event_id_datetime=datetime.datetime.now(),
            something="some type",
        )

        request = XxxServiceRequestDto(somethings=[u1, u2])
        json_compatible_item_data = jsonable_encoder(request)
        response = client.post(
            "/xxx/save_somethings", json=json_compatible_item_data
        )

        assert response.status_code == 200

        result = parse_obj_as(SomethingsSavingResultDto, json.loads(response.text))
        assert len(result.results) == 2
