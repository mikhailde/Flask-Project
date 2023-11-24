import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from flask import Flask
from app import app, db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    client = app.test_client()

    with app.app_context():
        db.create_all()

    yield client

    with app.app_context():
        db.drop_all()

def make_request(client, endpoint):
    return client.get(endpoint).data.decode('utf-8')

def test_index(client):
    response = make_request(client, '/')
    assert 'Главная' in response
    assert '200 OK' in response

def test_about(client):
    response = make_request(client, '/about')
    assert 'О компании' in response
    assert '200 OK' in response

def test_contact(client):
    response = make_request(client, '/contact')
    assert 'Обратная связь' in response
    assert '200 OK' in response

def test_event_catalog(client):
    response = make_request(client, '/event_catalog')
    assert 'Каталог мероприятий' in response
    assert '200 OK' in response
