import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import app, db


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
    client = app.test_client()
    yield client
    with app.app_context():
        db.drop_all()

def make_request(client, endpoint):
    return client.get(endpoint).data.decode('utf-8')

def test_index(client):
    assert 'Главная' in make_request(client, '/')

def test_about(client):
    assert 'О компании' in make_request(client, '/about')

def test_contact(client):
    assert 'Обратная связь' in make_request(client, '/contact')

def test_event_catalog(client):
    assert 'Каталог мероприятий' in make_request(client, '/event_catalog')

def test_get_token(client):
    assert client.get('/get_token').status_code == 401

def test_edit_profile(client):
    assert client.post('/edit_profile', json={'username': 'newusername', 'email': 'newemail@example.com'}).status_code == 302

def test_change_password(client):
    assert client.post('/change_password', json={'old_password': 'testpassword', 'new_password': 'newpassword'}).status_code == 302

def test_admin_dashboard(client):
    assert client.get('/admin_dashboard').status_code == 302

def test_edit_and_delete_event(client):
    assert client.post('/create_event', json={'title': 'Test Event', 'description': 'This is a test event.', 'date_time': '2023-12-01 12:00:00', 'location': 'Test Location'}).status_code == 302
    assert client.get('/edit_event/1').status_code == 302
    assert client.post('/delete_event').status_code == 302

def test_delete_user(client):
    assert client.post('/delete_user').status_code == 302
