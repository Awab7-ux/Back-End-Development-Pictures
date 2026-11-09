import copy
import json
from pathlib import Path

import pytest

import backend


PICTURES_PATH = Path(__file__).parents[1] / "backend" / "data" / "pictures.json"


@pytest.fixture(autouse=True)
def reset_pictures():
    original_pictures = json.loads(PICTURES_PATH.read_text(encoding="utf-8"))
    backend.data[:] = copy.deepcopy(original_pictures)


@pytest.fixture
def client():
    backend.app.config.update(TESTING=True)
    return backend.app.test_client()


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "OK"}


def test_count(client):
    response = client.get("/count")
    assert response.status_code == 200
    assert response.get_json() == {"length": 10}


def test_data_contains_10_pictures():
    assert len(backend.data) == 10


def test_get_picture(client):
    response = client.get("/picture")
    assert response.status_code == 200
    assert len(response.get_json()) == 10


def test_get_pictures_check_content_type_equals_json(client):
    response = client.get("/picture")
    assert response.content_type == "application/json"


def test_get_picture_by_id(client):
    response = client.get("/picture/1")
    assert response.status_code == 200
    assert response.get_json()["id"] == 1


def test_pictures_json_is_not_empty():
    pictures = json.loads(PICTURES_PATH.read_text(encoding="utf-8"))
    assert pictures


def test_get_picture_by_id_404(client):
    response = client.get("/picture/999")
    assert response.status_code == 404
    assert response.get_json() == {"message": "picture not found"}


def test_post_picture(client):
    picture = {
        "id": 11,
        "pic_url": "https://picsum.photos/id/1070/1200/800",
        "event_country": "Spain",
        "event_state": "Catalonia",
        "event_city": "Barcelona",
        "event_date": "2024-12-01",
    }
    response = client.post("/picture", json=picture)
    assert response.status_code == 201
    assert response.get_json() == picture
    assert len(backend.data) == 11


def test_post_picture_duplicate(client):
    response = client.post("/picture", json={"id": 1})
    assert response.status_code == 302
    assert response.get_json() == {"Message": "picture with id 1 already present"}


def test_update_picture_by_id(client):
    picture = {
        "id": 1,
        "pic_url": "https://picsum.photos/id/1011/1200/800",
        "event_country": "United States",
        "event_state": "California",
        "event_city": "Los Angeles",
        "event_date": "2025-01-15",
    }
    response = client.put("/picture/1", json=picture)
    assert response.status_code == 200
    assert response.get_json() == picture
    assert backend.data[0] == picture


def test_delete_picture_by_id(client):
    response = client.delete("/picture/10")
    assert response.status_code == 204
    assert response.data == b""
    assert len(backend.data) == 9