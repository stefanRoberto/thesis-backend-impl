import datetime

import pytest
from fastapi.encoders import jsonable_encoder

from tests.conftest import client


@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown(artist_create_schema):
    response = client.post(
        "/api/artists/",
        json=jsonable_encoder(artist_create_schema)
    )

    artist_id = response.json()['data']['id']

    yield artist_id

    client.delete(f"/api/artists/{artist_id}")


@pytest.fixture
def response_json():
    return {
        "id": 1,
        "title": "Test Album",
        "release_date": datetime.date.today().isoformat(),
        "artist_id": 1
    }


@pytest.fixture
def response_json_updated():
    return {
        "id": 1,
        "title": "Updated Test Album",
        "release_date": datetime.date(2000, 1, 1).isoformat(),
        "artist_id": 1
    }


def test_create_album(album_create_schema, response_json):
    response = client.post(
        "/api/albums/",
        json=jsonable_encoder(album_create_schema)
    )

    assert response.status_code == 201

    assert response.json()['code'] == 201
    assert response.json()['message'] == 'Album created successfully'
    assert response.json()['data'] == response_json


def test_create_album_error(album_create_schema, response_json):
    album_create_schema.artist_id = 10

    response = client.post(
        "/api/albums/",
        json=jsonable_encoder(album_create_schema)
    )

    assert response.status_code == 400

    assert response.json()['detail'] == 'Artist with id 10 does not exist'


def test_read_album(response_json):
    response = client.get("/api/albums/1")

    assert response.status_code == 200

    assert response.json()['code'] == 200
    assert response.json()['message'] == 'Album retrieved successfully'
    assert response.json()['data'] == response_json


def test_read_album_not_found():
    response = client.get("/api/albums/2")

    assert response.status_code == 404

    assert response.json()['detail'] == 'Album not found'


def test_update_album(album_update_schema, response_json_updated):
    response = client.patch(
        "/api/albums/1",
        json=jsonable_encoder(album_update_schema)
    )

    assert response.status_code == 200

    assert response.json()['code'] == 200
    assert response.json()['message'] == 'Album updated successfully'
    assert response.json()['data'] == response_json_updated


def test_update_album_not_found(album_update_schema):
    response = client.patch(
        "/api/albums/2",
        json=jsonable_encoder(album_update_schema)
    )

    assert response.status_code == 404

    assert response.json()['detail'] == 'Album not found'


def test_delete_album(response_json_updated):
    response = client.delete("/api/albums/1")

    assert response.status_code == 200

    assert response.json()['code'] == 200
    assert response.json()['message'] == 'Album deleted successfully'
    assert response.json()['data'] == response_json_updated


def test_delete_album_not_found():
    response = client.delete("/api/albums/2")

    assert response.status_code == 404

    assert response.json()['detail'] == 'Album not found'
