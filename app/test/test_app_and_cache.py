import pytest
from app import create_app
from app.cache import cache


@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
    })

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


def test_hello_world(client):
    res = client.get('/')
    assert res.status_code == 200
    assert b"Hello, World!" in res.data

def test_cache(client):
    with client:
        cache.set("test_key", "test_value")
        assert cache.get("test_key") == "test_value"
