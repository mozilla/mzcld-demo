from fastapi.testclient import TestClient
import pytest

from app.main import app


client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


def test_read_item():
    response = client.get("/items/5")
    assert response.status_code == 200
    assert response.json() == {"item_id": 5, "q": None}


def test_io_task():
    response = client.get("/io_task")
    assert response.status_code == 200
    assert response.json() == {"msg": "IO bound task finish!"}


def test_cpu_task():
    response = client.get("/cpu_task")
    assert response.status_code == 200
    assert response.json() == {"msg": "CPU bound task finish!"}


def test_random_status():
    response = client.get("/random_status")
    assert response.json() == {"path": "/random_status"}


def test_random_sleep():
    response = client.get("/random_sleep")
    assert response.status_code == 200
    assert response.json() == {"path": "/random_sleep"}


def test_unhandled_exception():
    with pytest.raises(ValueError):
        client.get("/unhandled_exception")


def test_http_exception():
    response = client.get("/http_exception")
    assert response.status_code == 500
    assert response.json() == {"detail": "http exception"}
