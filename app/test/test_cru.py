import pytest
from app import create_app
from app.models import Sport, Event, Selection
from app.db import get_db

@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
    })

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


# TODO: improve test coverage to 100%
# TODO: test for exceptions

def test_create_sport(client):
    payload = {'name': 'Test Sport', 
               'slug': 'test-sport', 
               'active': True}
    response = client.post('/sports', json=payload)
    assert response.status_code == 201
    assert 'Sport created successfully' in response.get_json()['message']

def test_update_sport(client):
    payload = {'name': 'Test Sport', 
               'slug': 'test-sport-updated', 
               'active': True}
    response = client.put('/sports/1', json=payload)
    assert response.status_code == 200
    assert 'Sport updated successfully' in response.get_json()['message']


def test_search_sport(client):
    response = client.get('/sports/search?name_regex=test')
    assert response.status_code == 200
    assert 'Test Sport' in response.get_json()[0]['name']


def test_create_event(client):
    payload = {'name': 'Test Sport Finals', 
               'slug': 'test-sport-finals', 
               'active': True, 
               'sport': 1, 
               'scheduled_start': '2024-07-17T01:00:00Z', 
               'status': 'Pending', 
               'type': 'preplay'}
    response = client.post('/events', json=payload)
    assert response.status_code == 201
    assert 'Event created successfully' in response.get_json()['message']


def test_update_event(client):
    payload = {'name': 'Test Sport Finals', 
               'slug': 'test-sport-finals-updated', 
               'active': True, 
               'sport': 1, 
               'scheduled_start': '2024-07-17T01:00:00Z', 
               'status': 'Pending', 
               'type': 'preplay'}
    response = client.put('/events/1', json=payload)
    assert response.status_code == 200
    assert 'Event updated successfully' in response.get_json()['message']


def test_search_event(client):
    response = client.get('/events/search?name_regex=test')
    assert response.status_code == 200
    assert 'Test Sport Finals' in response.get_json()[0]['name']


def test_create_selection(client):
    payload = {'name': 'Test Win', 
               'event': 1, 
               'price': 1.5, 
               'active': True, 
               'outcome': 'Unsettled'}
    response = client.post('/selections', json=payload)
    assert response.status_code == 201
    assert 'Selection created successfully' in response.get_json()['message']


def test_update_selection(client):
    payload = {'name': 'Test Win Updated', 
               'event': 1, 
               'price': 1.8, 
               'active': True, 
               'outcome': 'Unsettled'}
    response = client.put('/selections/1', json=payload)
    assert response.status_code == 200
    assert 'Selection updated successfully' in response.get_json()['message']


def test_search_selection(client):
    response = client.get('/selections/search?name_regex=test')
    assert response.status_code == 200
    assert 'Test Win' in response.get_json()[0]['name']
