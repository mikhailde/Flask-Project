import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tempfile
from app.utils import save_event_photo, process_event_photo
from werkzeug.datastructures import FileStorage
from flask import Flask

app = Flask(__name__)
app.config['UPLOADS_DEFAULT_DEST'] = 'app/static/uploads'

class MockPhoto:
    def __init__(self, filename):
        self.data = FileStorage(
            stream=open(filename, "rb"),
            filename="test.jpg",
            content_type="image/jpeg",
        )

class MockForm:
    def __init__(self, filename):
        self.photo = MockPhoto(filename)

def test_save_event_photo():
    _, temp_filename = tempfile.mkstemp(suffix=".jpg")
    with open(temp_filename, "w") as temp_file:
        temp_file.write("Temporary image content")

    with open(temp_filename, "rb") as temp_file:
        photo = FileStorage(temp_file)

        save_event_photo(photo, "test_photo.jpg")

        photo_path = os.path.join(app.config['UPLOADS_DEFAULT_DEST'], "test_photo.jpg")
        assert os.path.exists(photo_path)

def test_process_event_photo():
    _, temp_filename = tempfile.mkstemp(suffix=".jpg")
    with open(temp_filename, "w") as temp_file:
        temp_file.write("Temporary image content")

    form = MockForm(temp_filename)

    filename = process_event_photo(form)

    assert os.path.exists(os.path.join(app.config['UPLOADS_DEFAULT_DEST'], filename))
    assert filename == "test.jpg"
