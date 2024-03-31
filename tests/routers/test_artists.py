import datetime

import pytest
from fastapi.encoders import jsonable_encoder

from tests.conftest import client


@pytest.fixture
def response_json():
    return {
        "id": 1,
        "name": "Test Artist",
        "country": "UK",
        "birth_date": datetime.date.today().isoformat(),
        "bio": "Test bio",
        "genre": "Test genre",
        "listeners": 0
    }


@pytest.fixture
def response_json_updated():
    return {
        "id": 1,
        "name": "Test Artist",
        "country": "UK",
        "birth_date": datetime.date.today().isoformat(),
        "bio": "Updated test bio",
        "genre": "Updated test genre",
        "listeners": 0
    }


def test_create_artist(artist_create_schema, response_json):
    response = client.post(
        "/api/artists/",
        json=jsonable_encoder(artist_create_schema)
    )

    assert response.status_code == 201

    assert response.json()['code'] == 201
    assert response.json()['message'] == 'Artist created successfully'
    assert response.json()['data'] == response_json


def test_read_artist(response_json):
    response = client.get("/api/artists/1")

    assert response.status_code == 200

    assert response.json()['code'] == 200
    assert response.json()['message'] == 'Artist retrieved successfully'
    assert response.json()['data'] == response_json


def test_read_artist_not_found():
    response = client.get("/api/artists/2")

    assert response.status_code == 404

    assert response.json()['detail'] == 'Artist not found'


def test_update_artist(artist_update_schema, response_json_updated):
    response = client.patch(
        "/api/artists/1",
        json=jsonable_encoder(artist_update_schema)
    )

    assert response.status_code == 200

    assert response.json()['code'] == 200
    assert response.json()['message'] == 'Artist updated successfully'
    assert response.json()['data'] == response_json_updated


def test_update_artist_not_found(artist_update_schema):
    response = client.patch(
        "/api/artists/2",
        json=jsonable_encoder(artist_update_schema)
    )

    assert response.status_code == 404

    assert response.json()['detail'] == 'Artist not found'


def test_delete_artist(response_json_updated):
    response = client.delete("/api/artists/1")

    assert response.status_code == 200

    assert response.json()['code'] == 200
    assert response.json()['message'] == 'Artist deleted successfully'
    assert response.json()['data'] == response_json_updated


def test_delete_artist_not_found():
    response = client.delete("/api/artists/2")

    assert response.status_code == 404

    assert response.json()['detail'] == 'Artist not found'
