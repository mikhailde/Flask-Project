import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app.models import User, Event
from datetime import datetime



@pytest.fixture
def sample_user():
    user = User(username='testuser', email='testuser@example.com')
    user.set_password('testpassword')
    return user

@pytest.fixture
def sample_event(sample_user):
    return Event(title='Test Event', description='Test Description', date_time=datetime.utcnow(), location='Test Location', organizer=sample_user)

def test_user_creation(sample_user):
    assert sample_user.username == 'testuser'
    assert sample_user.email == 'testuser@example.com'
    assert sample_user.check_password('testpassword')

def test_event_creation(sample_event, sample_user):
    assert sample_event.title == 'Test Event'
    assert sample_event.description == 'Test Description'
    assert sample_event.date_time
    assert sample_event.location == 'Test Location'
    assert sample_event.organizer == sample_user

def test_event_representation(sample_event):
    assert repr(sample_event) == f"Event('Test Event', '{sample_event.date_time}')"

def test_user_representation(sample_user):
    assert repr(sample_user) == f"User('testuser', 'testuser@example.com')"