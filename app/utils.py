from datetime import datetime
from flask import render_template, request
from werkzeug.utils import secure_filename
from app import app

current_year = datetime.now().year

def render_template_with_cookies(template_name, **kwargs):
    cookies_accepted = get_cookie("cookies_accepted") == "true"
    return render_template(template_name, cookies_accepted=cookies_accepted, **kwargs)


def save_event_photo(photo, filename):
    photo_path = app.config['UPLOADS_DEFAULT_DEST']
    photo.save(f'{photo_path}/{filename}')


def process_event_photo(form):
    photo = form.photo.data
    if photo:
        filename = secure_filename(photo.filename)
        save_event_photo(photo, filename)
        return filename
    return None


def get_cookie(name):
    return request.cookies.get(name, "")
