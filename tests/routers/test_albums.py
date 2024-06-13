import datetime

import pytest
from fastapi.encoders import jsonable_encoder

from tests.conftest import client


def test_create_album_error():
    response = client.post(
        "/api/albums/",
        json=jsonable_encoder(
            {"title": "Test Album", "release_date": datetime.date.today().isoformat(), "artist_id": 1})
    )

    assert response.status_code == 400
    assert response.json()['detail'] == 'Artist with id 1 does not exist'
